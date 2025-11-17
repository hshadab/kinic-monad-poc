"""
Kinic Memory Agent - FastAPI Service
Integrates Kinic (IC) memory storage with Monad blockchain logging
"""
import os
import sys
from dotenv import load_dotenv

# Force UTF-8 encoding for stdout/stderr BEFORE anything else
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# Load environment variables FIRST before any other imports
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from pathlib import Path

from src.models import (
    InsertRequest, SearchRequest, InsertResponse,
    SearchResponse, SearchResult, HealthResponse,
    ChatRequest, ChatResponse
)
from src.kinic_client import KinicClient
from src.metadata import extract_metadata
from src.monad import MonadLogger
from src.ai_agent import AIAgent
from src.credential_manager import get_credential_manager, CredentialKey


# Global instances
kinic: KinicClient = None
monad: MonadLogger = None
ai_agent: AIAgent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    global kinic, monad, ai_agent

    print("\n" + "="*60)
    print("Starting Kinic Memory Agent on Monad")
    print("="*60)

    # Get credential manager
    cred_mgr = get_credential_manager()

    # Load configuration from keyring with fallback to environment variables
    print("\nLoading credentials from OS keyring...")
    memory_id = cred_mgr.get_credential(CredentialKey.KINIC_MEMORY_ID, fallback_env_var="KINIC_MEMORY_ID")
    identity_pem = os.getenv("IC_IDENTITY_PEM", "")  # PEM content from environment
    ic_url = os.getenv("IC_URL", "https://ic0.app")
    monad_rpc = cred_mgr.get_credential(CredentialKey.MONAD_RPC_URL, fallback_env_var="MONAD_RPC_URL") or "https://testnet-rpc.monad.xyz"
    monad_key = cred_mgr.get_credential(CredentialKey.MONAD_PRIVATE_KEY, fallback_env_var="MONAD_PRIVATE_KEY")
    monad_contract = os.getenv("MONAD_CONTRACT_ADDRESS")  # Keep this as env var for now
    anthropic_key = cred_mgr.get_credential(CredentialKey.ANTHROPIC_API_KEY, fallback_env_var="ANTHROPIC_API_KEY")

    # Validate required credentials
    if not memory_id:
        raise ValueError("KINIC_MEMORY_ID not found in keyring or environment variables. Run setup_credentials.py first.")
    if not identity_pem:
        print("Warning: IC_IDENTITY_PEM not set, using anonymous identity for IC")
    if not monad_key:
        raise ValueError("MONAD_PRIVATE_KEY not found in keyring or environment variables. Run setup_credentials.py first.")
    if not monad_contract:
        raise ValueError("MONAD_CONTRACT_ADDRESS environment variable required")
    if not anthropic_key:
        raise ValueError("ANTHROPIC_API_KEY not found in keyring or environment variables. Run setup_credentials.py first.")

    print("Credentials loaded successfully")

    # Initialize Kinic client (Python IC client)
    print("\nInitializing Kinic Client (Python IC)...")
    kinic = KinicClient(
        memory_id=memory_id,
        identity_pem=identity_pem,
        ic_url=ic_url
    )

    # Initialize Monad logger
    print("\nInitializing Monad Logger...")
    monad = MonadLogger(
        rpc_url=monad_rpc,
        private_key=monad_key,
        contract_address=monad_contract
    )

    # Initialize AI Agent
    print("\nInitializing AI Agent (Claude Haiku)...")
    ai_agent = AIAgent(
        api_key=anthropic_key,
        model="claude-3-haiku-20240307"  # Fast and cheap
    )

    print("\n" + "="*60)
    print("All services initialized successfully!")
    print("="*60 + "\n")

    yield

    # Cleanup on shutdown
    print("\nShutting down...")


# Create FastAPI app
app = FastAPI(
    title="Kinic Memory Agent on Monad",
    description="AI memory agent using Kinic (IC) for storage and Monad for rich metadata logging",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add response headers to prevent caching
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Prevent caching of HTML and JavaScript files
        if request.url.path.endswith(('.html', '.js', '.css')):
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response

app.add_middleware(NoCacheMiddleware)


@app.get("/api", response_model=dict)
async def api_root():
    """API root endpoint"""
    return {
        "service": "Kinic Memory Agent on Monad",
        "status": "running",
        "endpoints": {
            "insert": "POST /insert",
            "search": "POST /search",
            "health": "GET /health",
            "chat": "POST /chat",
            "stats": "GET /stats"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""

    kinic_status = "connected" if kinic else "not initialized"
    monad_status = "connected" if monad and monad.w3.is_connected() else "disconnected"

    return HealthResponse(
        status="healthy" if kinic and monad else "degraded",
        kinic=kinic_status,
        monad=monad_status,
        memory_id=os.getenv("KINIC_MEMORY_ID")
    )


@app.post("/insert", response_model=InsertResponse)
async def insert_memory(request: InsertRequest):
    """
    Insert content into Kinic memory and log metadata to Monad

    Flow:
    1. Store content in Kinic (via IC)
    2. Extract metadata (title, summary, tags, hash)
    3. Log rich metadata to Monad blockchain
    4. Return results
    """
    if not kinic or not monad:
        raise HTTPException(status_code=503, detail="Services not initialized")

    try:
        print(f"\n INSERT request received ({len(request.content)} chars)")

        # 1. Insert into Kinic memory (Internet Computer)
        print("  -> Storing in Kinic...")
        kinic_result = None
        try:
            kinic_result = await kinic.insert(
                content=request.content,
                tag=request.user_tags or "general"
            )
            print(f"   Stored in Kinic")
        except Exception as e:
            # Handle Kinic errors gracefully
            error_msg = str(e)
            print(f"    Kinic insert failed: {error_msg}")
            print(f"    Full error: {repr(e)}")
            print("     Will log to Monad only")
            kinic_result = {"status": "skipped", "reason": error_msg[:100]}

        # 2. Extract metadata
        print("  -> Extracting metadata...")
        metadata = extract_metadata(request.content, request.user_tags)
        print(f"   Title: '{metadata.title[:50]}...'")
        print(f"   Tags: {metadata.tags}")

        # 3. Log to Monad with rich metadata
        print("  -> Logging to Monad blockchain...")
        monad_tx = await monad.log_insert(
            title=metadata.title,
            summary=metadata.summary,
            tags=metadata.tags,
            content_hash=metadata.content_hash
        )
        print(f"   Logged to Monad: {monad_tx[:16]}...")

        print(f" INSERT completed successfully!\n")

        return InsertResponse(
            kinic_result=kinic_result,
            monad_tx=monad_tx,
            metadata=metadata
        )

    except Exception as e:
        print(f" INSERT failed: {e}\n")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", response_model=SearchResponse)
async def search_memory(request: SearchRequest):
    """
    Search Kinic memory and log search to Monad

    Flow:
    1. Search Kinic memory (via IC)
    2. Extract query metadata
    3. Log search operation to Monad
    4. Return results
    """
    if not kinic or not monad:
        raise HTTPException(status_code=503, detail="Services not initialized")

    try:
        print(f"\n SEARCH request: '{request.query}'")

        # 1. Search Kinic memory
        print("  -> Searching Kinic...")
        kinic_results = await kinic.search(
            query=request.query,
            top_k=request.top_k
        )
        print(f"   Found {len(kinic_results)} results")

        # 2. Extract query metadata
        print("  -> Extracting metadata...")
        metadata = extract_metadata(request.query, "search")

        # 3. Log search to Monad
        print("  -> Logging search to Monad...")
        monad_tx = await monad.log_search(
            title=f"Search: {metadata.title}",
            summary=metadata.summary,
            tags=metadata.tags,
            content_hash=metadata.content_hash
        )
        print(f"   Logged to Monad: {monad_tx[:16]}...")

        # 4. Format results
        results = []
        for item in kinic_results[:request.top_k]:
            results.append(SearchResult(
                score=item.get("score", 1.0),
                text=item.get("text", str(item)),
                tag=item.get("tag")
            ))

        print(f" SEARCH completed successfully!\n")

        return SearchResponse(
            results=results,
            monad_tx=monad_tx,
            num_results=len(results)
        )

    except Exception as e:
        print(f" SEARCH failed: {e}\n")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", response_model=dict)
async def get_stats():
    """Get statistics from Monad blockchain"""
    if not monad:
        raise HTTPException(status_code=503, detail="Monad not initialized")

    try:
        total_memories = monad.get_total_memories()
        user_memories = monad.get_user_memory_count(monad.account.address)

        return {
            "total_memories_on_chain": total_memories,
            "agent_memories": user_memories,
            "contract_address": os.getenv("MONAD_CONTRACT_ADDRESS"),
            "agent_address": monad.account.address
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/list-memories", response_model=dict)
async def list_memories(limit: int = 20, offset: int = 0):
    """List memories from Monad blockchain"""
    if not monad:
        raise HTTPException(status_code=503, detail="Monad not initialized")

    try:
        total_memories = monad.get_total_memories()
        user_memories_ids = []

        # Get all memory IDs for this user
        user_count = monad.get_user_memory_count(monad.account.address)

        # Fetch user's memories (most recent first)
        memories_list = []
        for i in range(max(0, user_count - offset - limit), min(user_count, user_count - offset)):
            memory_id = monad.contract.functions.userMemories(monad.account.address, i).call()
            memory_data = monad.get_memory(memory_id)

            # Only include INSERT operations (opType == 0), not SEARCH operations
            if memory_data["opType"] == 0:
                memories_list.append({
                    "id": memory_id,
                    "title": memory_data["title"],
                    "summary": memory_data["summary"],
                    "tags": memory_data["tags"],
                    "contentHash": memory_data["contentHash"],
                    "timestamp": memory_data["timestamp"],
                    "user": memory_data["user"]
                })

        # Reverse to show most recent first
        memories_list.reverse()

        return {
            "memories": memories_list,
            "total": user_count,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        print(f"Error listing memories: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Chat with AI agent (Claude) with memory context

    Flow:
    1. Search Kinic for relevant memories
    2. Pass memories as context to Claude
    3. Generate AI response
    4. Log conversation to Monad
    5. Return response
    """
    if not kinic or not monad or not ai_agent:
        raise HTTPException(status_code=503, detail="Services not initialized")

    try:
        print(f"\n CHAT request: '{request.message[:50]}...'")

        # 1. Search Kinic for relevant context
        print("  -> Searching Kinic for context...")
        memories = []

        try:
            kinic_results = await kinic.search(
                query=request.message,
                top_k=request.top_k
            )

            # Format results for AI agent
            for item in kinic_results[:request.top_k]:
                memories.append({
                    "text": item.get("sentence", item.get("text", str(item))),
                    "score": item.get("score", 1.0),
                    "tag": item.get("tag", "")
                })

            print(f"   Found {len(memories)} relevant memories")
        except Exception as e:
            # Handle Kinic errors gracefully
            print(f"    Kinic search failed: {str(e)}")
            print(f"    Full error: {repr(e)}")
            print("     Chat will work without memory context")
            memories = []
            print(f"   Found {len(memories)} relevant memories")

        # 2. Generate AI response with context
        print("  -> Generating AI response with Claude...")
        response_text = await ai_agent.chat(
            message=request.message,
            memory_context=memories
        )
        print(f"   AI response generated ({len(response_text)} chars)")

        # 3. Extract metadata for Monad logging
        print("  -> Logging conversation to Monad...")
        conversation_metadata = extract_metadata(
            f"User: {request.message}\nAgent: {response_text}",
            "chat,conversation"
        )

        # 4. Log to Monad
        monad_tx = await monad.log_insert(
            title=f"Chat: {conversation_metadata.title}",
            summary=conversation_metadata.summary,
            tags=conversation_metadata.tags,
            content_hash=conversation_metadata.content_hash
        )
        print(f"   Logged to Monad: {monad_tx[:16]}...")

        print(f" CHAT completed successfully!\n")

        return ChatResponse(
            response=response_text,
            memories_used=memories,
            num_memories=len(memories),
            monad_tx=monad_tx
        )

    except Exception as e:
        print(f" CHAT failed: {e}\n")
        raise HTTPException(status_code=500, detail=str(e))


# Serve Next.js frontend static files
FRONTEND_DIR = Path(__file__).parent.parent / "frontend" / "out"

if FRONTEND_DIR.exists():
    # Mount static files (CSS, JS, images, etc.)
    app.mount("/_next", StaticFiles(directory=FRONTEND_DIR / "_next"), name="static-next")

    # Serve root and all routes with index.html (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve Next.js frontend for all non-API routes"""
        # If it's an API route, return 404
        if full_path.startswith(("insert", "search", "chat", "health", "stats", "api")):
            raise HTTPException(status_code=404, detail="Not found")

        # Try to serve the exact file first (for static assets)
        file_path = FRONTEND_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)

        # Try with .html extension (Next.js static export)
        html_path = FRONTEND_DIR / f"{full_path}.html"
        if html_path.is_file():
            return FileResponse(html_path)

        # Default to index.html for SPA routing
        index_path = FRONTEND_DIR / "index.html"
        if index_path.is_file():
            return FileResponse(index_path)

        raise HTTPException(status_code=404, detail="Not found")
else:
    print("  Frontend not found - serving API only")


# Run locally for testing
if __name__ == "__main__":
    import uvicorn

    print(" Running in development mode...")
    print("  Make sure you have set all required environment variables!\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
