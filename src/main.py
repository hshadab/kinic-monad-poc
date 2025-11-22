"""
Kinic Memory Agent - FastAPI Service
Integrates Kinic (IC) memory storage with Monad blockchain logging
"""
import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

from src.auth import verify_api_key
from src.models import (
    InsertRequest, SearchRequest, InsertResponse,
    SearchResponse, SearchResult, HealthResponse,
    ChatRequest, ChatResponse,
    MonadSearchRequest, MonadSearchResponse, MonadMemory,
    MonadStatsResponse, TrendingTag
)
from src.kinic_client import KinicClient
from src.metadata import extract_metadata
from src.monad import MonadLogger
from src.monad_cache import MonadCache
from src.ai_agent import AIAgent
from src.credential_manager import get_credential_manager, CredentialKey


# Global instances
kinic: KinicClient = None
monad: MonadLogger = None
monad_cache: MonadCache = None
ai_agent: AIAgent = None

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    global kinic, monad, monad_cache, ai_agent

    print("\n" + "="*60)
    print("Starting Kinic Memory Agent on Monad")
    print("="*60)

    # Get credential manager
    cred_mgr = get_credential_manager()

    # Load configuration from keyring with fallback to environment variables
    print("\nLoading credentials from OS keyring...")
    memory_id = cred_mgr.get_credential(CredentialKey.KINIC_MEMORY_ID, fallback_env_var="KINIC_MEMORY_ID")
    identity_pem = os.getenv("IC_IDENTITY_PEM")  # PEM string for pure Python client
    monad_rpc = cred_mgr.get_credential(CredentialKey.MONAD_RPC_URL, fallback_env_var="MONAD_RPC_URL") or "https://testnet-rpc.monad.xyz"
    monad_key = cred_mgr.get_credential(CredentialKey.MONAD_PRIVATE_KEY, fallback_env_var="MONAD_PRIVATE_KEY")
    monad_contract = os.getenv("MONAD_CONTRACT_ADDRESS")  # Keep this as env var for now
    anthropic_key = cred_mgr.get_credential(CredentialKey.ANTHROPIC_API_KEY, fallback_env_var="ANTHROPIC_API_KEY")

    # Validate required credentials
    if not memory_id:
        raise ValueError("KINIC_MEMORY_ID not found in keyring or environment variables. Run setup_credentials.py first.")
    if not identity_pem:
        raise ValueError("IC_IDENTITY_PEM environment variable required for pure Python client")
    if not monad_key:
        raise ValueError("MONAD_PRIVATE_KEY not found in keyring or environment variables. Run setup_credentials.py first.")
    if not monad_contract:
        raise ValueError("MONAD_CONTRACT_ADDRESS environment variable required")
    if not anthropic_key:
        raise ValueError("ANTHROPIC_API_KEY not found in keyring or environment variables. Run setup_credentials.py first.")

    print("Credentials loaded successfully")

    # Initialize Kinic client (pure Python)
    print("\nInitializing Kinic Client (pure Python)...")
    kinic = KinicClient(memory_id=memory_id, identity_pem=identity_pem)

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

    # Initialize Monad Cache
    print("\nInitializing Monad Cache...")
    monad_cache = MonadCache(monad)

    # Sync cache from blockchain (async)
    await monad_cache.sync_from_blockchain()

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

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware - Secure configuration
# Get allowed origins from environment variable (comma-separated)
# Default includes production URL and common local development URLs
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "https://monad-ai-memory.onrender.com,http://localhost:3000,http://localhost:8000"
).split(",")

# If explicitly set to "*" in env, allow all (not recommended for production)
if allowed_origins == ["*"]:
    print("⚠️  WARNING: CORS set to allow all origins (*) - not recommended for production!")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Only necessary methods
    allow_headers=["Content-Type", "X-API-Key"],  # Only necessary headers
)


@app.get("/api", response_model=dict)
async def api_info():
    """API information endpoint"""
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
    """Health check endpoint with diagnostics"""

    kinic_status = "connected" if kinic else "not initialized"
    monad_status = "connected" if monad and monad.w3.is_connected() else "disconnected"

    # Log environment variable status for debugging
    env_status = {
        "KINIC_MEMORY_ID": "set" if os.getenv("KINIC_MEMORY_ID") else "MISSING",
        "IC_IDENTITY_PEM": "set" if os.getenv("IC_IDENTITY_PEM") else "MISSING",
        "MONAD_RPC_URL": "set" if os.getenv("MONAD_RPC_URL") else "using default",
        "MONAD_CONTRACT_ADDRESS": "set" if os.getenv("MONAD_CONTRACT_ADDRESS") else "MISSING",
        "MONAD_PRIVATE_KEY": "set" if os.getenv("MONAD_PRIVATE_KEY") else "MISSING",
        "ANTHROPIC_API_KEY": "set" if os.getenv("ANTHROPIC_API_KEY") else "MISSING",
    }

    print(f"Health check - Environment status: {env_status}")

    return HealthResponse(
        status="healthy" if kinic and monad else "degraded",
        kinic=kinic_status,
        monad=monad_status,
        memory_id=os.getenv("KINIC_MEMORY_ID")
    )


@app.post("/insert", response_model=InsertResponse)
@limiter.limit("20/minute")
async def insert_memory(req: Request, request: InsertRequest, api_key: str = Depends(verify_api_key)):
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
        if request.principal:
            print(f"   Using principal isolation: {request.principal[:10]}...")
        try:
            kinic_result = await kinic.insert(
                content=request.content,
                tag=request.user_tags or "general",
                principal=request.principal
            )
            print(f"   Stored in Kinic")
        except Exception as e:
            print(f"   Kinic storage failed: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Kinic storage failed: {str(e)}")

        # 2. Extract metadata
        print("  -> Extracting metadata...")
        metadata = extract_metadata(request.content, request.user_tags)
        print(f"   Title: '{metadata.title[:50]}...'")
        print(f"   Tags: {metadata.tags}")

        # 3. Log to Monad with rich metadata (include principal in tags for audit trail)
        print("  -> Logging to Monad blockchain...")
        monad_tags = metadata.tags
        if request.principal:
            monad_tags = f"{metadata.tags},principal:{request.principal}"
            print(f"   Including principal in on-chain metadata")

        try:
            monad_tx = await monad.log_insert(
                title=metadata.title,
                summary=metadata.summary,
                tags=monad_tags,
                content_hash=metadata.content_hash
            )
            print(f"   Logged to Monad: {monad_tx[:16]}...")
        except Exception as e:
            print(f"   Monad logging failed: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Monad blockchain logging failed: {str(e)}")

        print(f" INSERT completed successfully!\n")

        return InsertResponse(
            kinic_result=kinic_result,
            monad_tx=monad_tx,
            metadata=metadata
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f" INSERT failed: {e}\n")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", response_model=SearchResponse)
@limiter.limit("30/minute")
async def search_memory(req: Request, request: SearchRequest, api_key: str = Depends(verify_api_key)):
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
        if request.principal:
            print(f"   Filtering by principal: {request.principal[:10]}...")
        kinic_results = await kinic.search(
            query=request.query,
            top_k=request.top_k,
            principal=request.principal
        )
        print(f"   Found {len(kinic_results)} results")

        # 2. Extract query metadata
        print("  -> Extracting metadata...")
        metadata = extract_metadata(request.query, "search")

        # 3. Log search to Monad (include principal in tags for audit trail)
        print("  -> Logging search to Monad...")
        monad_tags = metadata.tags
        if request.principal:
            monad_tags = f"{metadata.tags},principal:{request.principal}"

        monad_tx = await monad.log_search(
            title=f"Search: {metadata.title}",
            summary=metadata.summary,
            tags=monad_tags,
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


@app.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat_with_agent(req: Request, request: ChatRequest, api_key: str = Depends(verify_api_key)):
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
        if request.principal:
            print(f"   Using principal: {request.principal[:10]}...")
        kinic_results = await kinic.search(
            query=request.message,
            top_k=request.top_k,
            principal=request.principal
        )

        # Format results for AI agent
        memories = []
        for item in kinic_results[:request.top_k]:
            memories.append({
                "text": item.get("sentence", item.get("text", str(item))),
                "score": item.get("score", 1.0),
                "tag": item.get("tag", "")
            })

        print(f"   Found {len(memories)} relevant memories")

        # 2. Generate AI response with context
        print("  -> Generating AI response with Claude...")

        # Create async wrapper for memories (ai_agent expects async search_function)
        async def _return_memories(q, k):
            return memories

        response_text, _ = await ai_agent.chat_with_memory_search(
            message=request.message,
            search_function=_return_memories,
            top_k=request.top_k
        )
        print(f"   AI response generated ({len(response_text)} chars)")

        # 3. Extract metadata for Monad logging
        print("  -> Logging conversation to Monad...")
        conversation_metadata = extract_metadata(
            f"User: {request.message}\nAgent: {response_text}",
            "chat,conversation"
        )

        # 4. Log to Monad (include principal in tags for audit trail)
        # Note: Monad logging failure should not block chat functionality
        monad_tx = "pending"
        try:
            monad_tags = conversation_metadata.tags
            if request.principal:
                monad_tags = f"{conversation_metadata.tags},principal:{request.principal}"

            monad_tx = await monad.log_insert(
                title=f"Chat: {conversation_metadata.title}",
                summary=conversation_metadata.summary,
                tags=monad_tags,
                content_hash=conversation_metadata.content_hash
            )
            print(f"   Logged to Monad: {monad_tx[:16]}...")
        except Exception as monad_error:
            print(f"   Monad logging failed (non-critical): {monad_error}")
            print(f"   Continuing with chat response...")
            monad_tx = f"failed: {str(monad_error)[:50]}"

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


@app.post("/monad/search", response_model=MonadSearchResponse)
async def search_monad_metadata(request: MonadSearchRequest):
    """
    Search Monad blockchain metadata cache

    Enables fast querying of on-chain memory logs without gas costs.
    Searches cached metadata by tags, title, or summary.

    Flow:
    1. Query local cache (synced from blockchain)
    2. Filter by tags, title, or summary
    3. Return matching memories with metadata
    """
    if not monad_cache:
        raise HTTPException(status_code=503, detail="Monad cache not initialized")

    if not monad_cache.synced:
        raise HTTPException(status_code=503, detail="Monad cache not synced yet")

    try:
        print(f"\n🔍 MONAD SEARCH request")

        results = []

        # Search by tags
        if request.tags:
            print(f"  -> Searching by tags: {request.tags}")
            results = monad_cache.search_by_tags(
                request.tags,
                limit=request.limit,
                op_type=request.op_type
            )
        # Search by title
        elif request.title:
            print(f"  -> Searching by title: {request.title}")
            results = monad_cache.search_by_title(
                request.title,
                limit=request.limit,
                op_type=request.op_type
            )
        # Search by summary
        elif request.summary:
            print(f"  -> Searching by summary: {request.summary}")
            results = monad_cache.search_by_summary(
                request.summary,
                limit=request.limit
            )
        # Get recent if no filters
        else:
            print(f"  -> Getting recent memories")
            results = monad_cache.get_recent(
                limit=request.limit,
                op_type=request.op_type
            )

        print(f"  ✅ Found {len(results)} results from Monad cache\n")

        # Convert to Pydantic models
        memory_models = [MonadMemory(**r) for r in results]

        return MonadSearchResponse(
            results=memory_models,
            num_results=len(memory_models),
            source="monad"
        )

    except Exception as e:
        print(f"❌ MONAD SEARCH failed: {e}\n")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/monad/stats", response_model=MonadStatsResponse)
async def get_monad_cache_stats():
    """
    Get Monad cache statistics

    Returns information about the cached blockchain data:
    - Total memories
    - Insert vs search operations
    - Unique tags and users
    - Most active user
    """
    if not monad_cache:
        raise HTTPException(status_code=503, detail="Monad cache not initialized")

    try:
        stats = monad_cache.get_stats()
        return MonadStatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/monad/trending", response_model=List[TrendingTag])
async def get_trending_tags(limit: int = 10):
    """
    Get trending tags from Monad metadata

    Returns most popular tags based on usage count.
    Useful for discovering what topics are being researched.

    Args:
        limit: Number of tags to return (default: 10)
    """
    if not monad_cache:
        raise HTTPException(status_code=503, detail="Monad cache not initialized")

    if not monad_cache.synced:
        raise HTTPException(status_code=503, detail="Monad cache not synced yet")

    try:
        trending = monad_cache.get_trending_tags(limit=limit)
        return [TrendingTag(tag=tag, count=count) for tag, count in trending]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/monad/refresh")
async def refresh_monad_cache():
    """
    Manually refresh Monad cache from blockchain

    Syncs all memories from Monad smart contract.
    Useful if cache gets out of sync.
    """
    if not monad_cache:
        raise HTTPException(status_code=503, detail="Monad cache not initialized")

    try:
        await monad_cache.refresh()
        stats = monad_cache.get_stats()
        return {
            "status": "refreshed",
            "total_memories": stats["total_memories"],
            "last_sync": stats["last_sync"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# FRONTEND STATIC FILES
# ============================================================================

# Mount static assets (_next folder with JS/CSS)
frontend_path = Path(__file__).parent.parent / "frontend" / "out"
if frontend_path.exists():
    app.mount("/_next", StaticFiles(directory=frontend_path / "_next"), name="static")

    # Serve specific HTML pages
    @app.get("/chat")
    async def serve_chat():
        return FileResponse(frontend_path / "chat.html")

    @app.get("/memories")
    async def serve_memories():
        return FileResponse(frontend_path / "memories.html")

    @app.get("/dashboard")
    async def serve_dashboard():
        return FileResponse(frontend_path / "dashboard.html")

    @app.get("/discover")
    async def serve_discover():
        return FileResponse(frontend_path / "discover.html")

    @app.get("/about")
    async def serve_about():
        return FileResponse(frontend_path / "about.html")

    # Serve index.html for root
    @app.get("/")
    async def serve_root():
        return FileResponse(frontend_path / "index.html")

    # Catch-all for SPA routing (404 fallback to index.html)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Don't intercept API routes
        if full_path.startswith(("api/", "health", "stats", "insert", "search")):
            raise HTTPException(status_code=404, detail="Not found")
        return FileResponse(frontend_path / "index.html")


# Run locally for testing
if __name__ == "__main__":
    import uvicorn

    print("🧪 Running in development mode...")
    print("⚠️  Make sure you have set all required environment variables!\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
