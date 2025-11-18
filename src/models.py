"""
Pydantic models for API requests/responses
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class Metadata(BaseModel):
    """Extracted metadata for Monad logging"""
    title: str = Field(..., max_length=100, description="Extracted title or heading")
    summary: str = Field(..., max_length=200, description="Content summary")
    tags: str = Field(..., description="Comma-separated keywords")
    content_hash: str = Field(..., description="SHA256 hash of content")


class InsertRequest(BaseModel):
    """Request to insert memory"""
    content: str = Field(..., description="Content to store in memory")
    user_tags: Optional[str] = Field("", description="Optional user-provided tags")

    class Config:
        json_schema_extra = {
            "example": {
                "content": "# ZKML\nJolt Atlas enables zero-knowledge proofs for ML inference...",
                "user_tags": "zkml,research"
            }
        }


class SearchRequest(BaseModel):
    """Request to search memory"""
    query: str = Field(..., min_length=1, description="Search query")
    top_k: Optional[int] = Field(5, ge=1, le=20, description="Number of results to return")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "How does zkml verification work?",
                "top_k": 5
            }
        }


class InsertResponse(BaseModel):
    """Response from insert operation"""
    kinic_result: Dict = Field(..., description="Result from Kinic CLI")
    monad_tx: str = Field(..., description="Monad transaction hash")
    metadata: Metadata = Field(..., description="Extracted metadata")


class SearchResult(BaseModel):
    """Individual search result"""
    score: float = Field(..., description="Relevance score")
    text: str = Field(..., description="Matching text content")
    tag: Optional[str] = Field(None, description="Associated tag")


class SearchResponse(BaseModel):
    """Response from search operation"""
    results: List[SearchResult] = Field(..., description="Search results")
    monad_tx: str = Field(..., description="Monad transaction hash")
    num_results: int = Field(..., description="Number of results returned")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    kinic: str
    monad: str
    memory_id: Optional[str] = None


class ChatRequest(BaseModel):
    """Request to chat with AI agent"""
    message: str = Field(..., min_length=1, description="User message")
    top_k: Optional[int] = Field(3, ge=1, le=10, description="Number of memories to use as context")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Tell me about ZKML",
                "top_k": 3
            }
        }


class ChatResponse(BaseModel):
    """Response from AI agent"""
    response: str = Field(..., description="AI-generated response")
    memories_used: List[Dict] = Field(..., description="Memories used as context")
    num_memories: int = Field(..., description="Number of memories retrieved")
    monad_tx: str = Field(..., description="Monad transaction hash for logging")


# Monad-specific models
class MonadMemory(BaseModel):
    """Memory metadata from Monad blockchain"""
    id: int = Field(..., description="On-chain memory ID")
    user: str = Field(..., description="User/agent Ethereum address")
    opType: int = Field(..., description="Operation type: 0=INSERT, 1=SEARCH")
    title: str = Field(..., description="Memory title")
    summary: str = Field(..., description="Content summary")
    tags: str = Field(..., description="Comma-separated tags")
    contentHash: str = Field(..., description="SHA256 hash of content")
    timestamp: int = Field(..., description="Unix timestamp")


class MonadSearchRequest(BaseModel):
    """Request to search Monad metadata"""
    tags: Optional[str] = Field(None, description="Comma-separated tags to search")
    title: Optional[str] = Field(None, description="Title substring to search")
    summary: Optional[str] = Field(None, description="Summary substring to search")
    op_type: Optional[int] = Field(None, ge=0, le=1, description="Filter by operation type")
    limit: Optional[int] = Field(50, ge=1, le=100, description="Maximum results")

    class Config:
        json_schema_extra = {
            "example": {
                "tags": "zkml,research",
                "limit": 20
            }
        }


class MonadSearchResponse(BaseModel):
    """Response from Monad metadata search"""
    results: List[MonadMemory] = Field(..., description="Matching memories")
    num_results: int = Field(..., description="Number of results")
    source: str = Field("monad", description="Data source")


class MonadStatsResponse(BaseModel):
    """Monad cache statistics"""
    synced: bool = Field(..., description="Cache sync status")
    last_sync: Optional[str] = Field(None, description="Last sync timestamp")
    total_memories: int = Field(..., description="Total memories cached")
    insert_operations: int = Field(..., description="Number of INSERT operations")
    search_operations: int = Field(..., description="Number of SEARCH operations")
    unique_tags: int = Field(..., description="Number of unique tags")
    unique_users: int = Field(..., description="Number of unique users")
    most_active_user: Optional[str] = Field(None, description="Most active user address")


class TrendingTag(BaseModel):
    """Trending tag with usage count"""
    tag: str = Field(..., description="Tag name")
    count: int = Field(..., description="Usage count")
