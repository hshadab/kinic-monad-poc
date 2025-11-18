"""
Simple API Key Authentication Middleware
"""
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from typing import Optional
import os

# API Key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: Optional[str] = Security(api_key_header)):
    """
    Verify API key from request header

    Args:
        api_key: API key from X-API-Key header

    Raises:
        HTTPException: If API key is missing or invalid
    """
    # Get valid API key from environment
    valid_api_key = os.getenv("API_KEY")

    # If no API_KEY set in env, allow all requests (backward compatibility)
    if not valid_api_key:
        return None

    # Check if API key provided
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key. Include X-API-Key header."
        )

    # Verify API key
    if api_key != valid_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )

    return api_key
