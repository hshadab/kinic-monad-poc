# API Authentication Guide

## Overview

The Kinic Memory Agent API now uses **API Key authentication** to protect critical endpoints and prevent unauthorized access. This guide explains how the authentication system works, how to use it, and what changes you need to make.

---

## Table of Contents

- [How Authentication Works](#how-authentication-works)
- [Protected Endpoints](#protected-endpoints)
- [Making Authenticated Requests](#making-authenticated-requests)
- [Frontend Integration](#frontend-integration)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Testing Authentication](#testing-authentication)
- [Security Best Practices](#security-best-practices)

---

## How Authentication Works

### 1. API Key Mechanism

The API uses a simple but effective **API Key** system:

```
┌─────────┐                      ┌──────────┐                    ┌─────────┐
│ Client  │                      │ FastAPI  │                    │ Backend │
└────┬────┘                      └────┬─────┘                    └────┬────┘
     │                                │                               │
     │  POST /insert                  │                               │
     │  Headers:                      │                               │
     │    X-API-Key: abc123           │                               │
     ├───────────────────────────────►│                               │
     │                                │                               │
     │                                │  1. Extract X-API-Key header  │
     │                                │  2. Compare with API_KEY env  │
     │                                │                               │
     │                                │  If valid:                    │
     │                                ├──────────────────────────────►│
     │                                │   Execute endpoint            │
     │                                │◄──────────────────────────────┤
     │◄───────────────────────────────┤   Return response             │
     │  200 OK                        │                               │
     │                                │                               │
     │                                │  If invalid/missing:          │
     │◄───────────────────────────────┤                               │
     │  401 Unauthorized              │                               │
     │  {"detail": "Invalid API Key"} │                               │
     │                                │                               │
```

### 2. Implementation Details

**File:** `src/auth.py`

```python
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
import os

# Define API key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: Optional[str] = Security(api_key_header)):
    """
    Verify API key from request header

    Returns None if valid, raises HTTPException if invalid
    """
    # Get valid API key from environment
    valid_api_key = os.getenv("API_KEY")

    # If no API_KEY set, allow all requests (backward compatible)
    if not valid_api_key:
        return None

    # Check if API key provided
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key. Include X-API-Key header."
        )

    # Verify API key matches
    if api_key != valid_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )

    return api_key
```

### 3. Endpoint Protection

**File:** `src/main.py`

```python
from src.auth import verify_api_key
from fastapi import Depends

# Protected endpoint example
@app.post("/insert", response_model=InsertResponse)
@limiter.limit("20/minute")  # Rate limiting
async def insert_memory(
    req: Request,
    request: InsertRequest,
    api_key: str = Depends(verify_api_key)  # ← Authentication
):
    # Only executes if API key is valid
    # ... endpoint logic ...
```

**Key Points:**
- `Depends(verify_api_key)` - FastAPI dependency injection
- Runs **before** the endpoint logic
- Automatically returns 401 if authentication fails
- No need for manual validation in endpoint code

---

## Protected Endpoints

### Endpoints Requiring Authentication

| Endpoint | Method | Rate Limit | Purpose |
|----------|--------|------------|---------|
| `/insert` | POST | 20/min | Insert memory into Kinic + Monad |
| `/search` | POST | 30/min | Search memories semantically |
| `/chat` | POST | 10/min | AI chat with memory context |

### Public Endpoints (No Auth Required)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/stats` | GET | Blockchain statistics |
| `/api` | GET | API information |
| `/` | GET | Homepage (static) |
| `/about` | GET | About page (static) |

---

## Making Authenticated Requests

### Using cURL

```bash
# Generate API key first
export API_KEY="your-secret-api-key-here"

# Example: Insert memory
curl -X POST https://monad-ai-memory.onrender.com/insert \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "content": "Important research notes about ZKML",
    "user_tags": "research,zkml"
  }'

# Example: Search memories
curl -X POST https://monad-ai-memory.onrender.com/search \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "query": "zero knowledge proofs",
    "top_k": 5
  }'

# Example: Chat with AI
curl -X POST https://monad-ai-memory.onrender.com/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "message": "What do I know about ZKML?",
    "top_k": 3
  }'
```

### Using Python (requests)

```python
import requests
import os

# Get API key from environment
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://monad-ai-memory.onrender.com"

# Headers with API key
headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

# Insert memory
response = requests.post(
    f"{BASE_URL}/insert",
    headers=headers,
    json={
        "content": "Important research notes",
        "user_tags": "research"
    }
)

if response.status_code == 200:
    result = response.json()
    print(f"Success! Monad TX: {result['monad_tx']}")
elif response.status_code == 401:
    print("Authentication failed - check your API key")
elif response.status_code == 429:
    print("Rate limit exceeded - wait a minute")
else:
    print(f"Error: {response.status_code}")
```

### Using JavaScript (fetch)

```javascript
const API_KEY = process.env.NEXT_PUBLIC_API_KEY;
const BASE_URL = 'https://monad-ai-memory.onrender.com';

// Insert memory
async function insertMemory(content, tags) {
  const response = await fetch(`${BASE_URL}/insert`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': API_KEY  // ← Required
    },
    body: JSON.stringify({
      content: content,
      user_tags: tags
    })
  });

  if (response.status === 401) {
    throw new Error('Invalid or missing API key');
  }

  if (response.status === 429) {
    throw new Error('Rate limit exceeded');
  }

  return await response.json();
}

// Usage
try {
  const result = await insertMemory('Test content', 'test');
  console.log('Memory inserted:', result.monad_tx);
} catch (error) {
  console.error('Error:', error.message);
}
```

---

## Frontend Integration

### Environment Variable Setup

**File:** `frontend/.env.local` (create this file)

```bash
# API Configuration
NEXT_PUBLIC_API_KEY=your-secret-api-key-here
NEXT_PUBLIC_API_URL=https://monad-ai-memory.onrender.com
```

### API Client Configuration

**File:** `frontend/lib/api.ts` (update existing file)

```typescript
// API configuration
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || '';
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';

// Create axios instance with auth header
import axios from 'axios';

const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY  // ← Automatically included in all requests
  }
});

// Export API methods
export const api = {
  insertMemory: async (content: string, tags: string) => {
    const response = await apiClient.post('/insert', {
      content,
      user_tags: tags
    });
    return response.data;
  },

  searchMemories: async (query: string, topK: number = 5) => {
    const response = await apiClient.post('/search', {
      query,
      top_k: topK
    });
    return response.data;
  },

  chatWithAI: async (message: string, topK: number = 3) => {
    const response = await apiClient.post('/chat', {
      message,
      top_k: topK
    });
    return response.data;
  }
};

// Error handling interceptor
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      console.error('Authentication failed - check API key');
    } else if (error.response?.status === 429) {
      console.error('Rate limit exceeded - please wait');
    }
    return Promise.reject(error);
  }
);
```

### Using in Components

```typescript
import { api } from '@/lib/api';

export default function ChatPage() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleChat = async () => {
    try {
      const result = await api.chatWithAI(message, 3);
      setResponse(result.response);
    } catch (error) {
      if (error.response?.status === 401) {
        alert('Authentication error - API key invalid');
      } else if (error.response?.status === 429) {
        alert('Too many requests - please wait a minute');
      } else {
        alert('Error: ' + error.message);
      }
    }
  };

  return (
    // ... component JSX
  );
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Name | Meaning | Action |
|------|------|---------|--------|
| 200 | OK | Request successful | Continue |
| 401 | Unauthorized | Missing or invalid API key | Check `X-API-Key` header |
| 429 | Too Many Requests | Rate limit exceeded | Wait 60 seconds |
| 500 | Internal Server Error | Server error | Check logs |
| 503 | Service Unavailable | Services not initialized | Wait and retry |

### Error Response Format

**401 Unauthorized (Missing Key):**
```json
{
  "detail": "Missing API Key. Include X-API-Key header."
}
```

**401 Unauthorized (Invalid Key):**
```json
{
  "detail": "Invalid API Key"
}
```

**429 Too Many Requests:**
```json
{
  "detail": "Rate limit exceeded: 20 per 1 minute"
}
```

### Handling Errors in Code

```python
import requests

def safe_api_call(endpoint, data):
    try:
        response = requests.post(
            f"{BASE_URL}/{endpoint}",
            headers={"X-API-Key": API_KEY},
            json=data
        )

        # Raise exception for HTTP errors
        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("❌ Authentication failed - check your API key")
        elif e.response.status_code == 429:
            print("⏳ Rate limit exceeded - wait 60 seconds")
        else:
            print(f"❌ HTTP Error: {e.response.status_code}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None
```

---

## Rate Limiting

### Rate Limits by Endpoint

Rate limiting is **per IP address**:

```python
# From src/main.py

@limiter.limit("20/minute")  # Max 20 requests per minute
async def insert_memory(...):
    pass

@limiter.limit("30/minute")  # Max 30 requests per minute
async def search_memory(...):
    pass

@limiter.limit("10/minute")  # Max 10 requests per minute
async def chat_with_agent(...):
    pass
```

### Why Different Limits?

- **Chat (10/min):** Most expensive (uses Claude AI)
- **Insert (20/min):** Writes to blockchain (gas costs)
- **Search (30/min):** Read-only, less resource intensive

### Handling Rate Limits

**Exponential Backoff:**
```python
import time

def insert_with_retry(content, tags, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(...)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = (2 ** attempt) * 60  # 1min, 2min, 4min
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

---

## Testing Authentication

### Test Script

**File:** `test_api_auth.py`

```python
#!/usr/bin/env python3
"""Test API authentication and rate limiting"""

import os
import requests
import time

BASE_URL = "https://monad-ai-memory.onrender.com"
API_KEY = os.getenv("API_KEY", "test-key")

def test_no_auth():
    """Test request without API key (should fail)"""
    print("\n1. Testing without API key...")
    response = requests.post(f"{BASE_URL}/insert", json={"content": "test"})
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print("   ✅ Correctly rejected (401)")

def test_invalid_auth():
    """Test request with invalid API key (should fail)"""
    print("\n2. Testing with invalid API key...")
    response = requests.post(
        f"{BASE_URL}/insert",
        headers={"X-API-Key": "wrong-key"},
        json={"content": "test"}
    )
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print("   ✅ Correctly rejected (401)")

def test_valid_auth():
    """Test request with valid API key (should succeed)"""
    print("\n3. Testing with valid API key...")
    response = requests.post(
        f"{BASE_URL}/insert",
        headers={"X-API-Key": API_KEY},
        json={"content": "Test memory", "user_tags": "test"}
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("   ✅ Accepted (200)")
    print(f"   Monad TX: {response.json()['monad_tx'][:16]}...")

def test_rate_limit():
    """Test rate limiting (should get 429 after limit)"""
    print("\n4. Testing rate limiting (chat endpoint - 10/min)...")

    # Make 11 requests quickly
    for i in range(11):
        response = requests.post(
            f"{BASE_URL}/chat",
            headers={"X-API-Key": API_KEY},
            json={"message": f"test {i}", "top_k": 1}
        )

        if response.status_code == 429:
            print(f"   ✅ Rate limited after {i+1} requests")
            return
        elif i < 10:
            print(f"   Request {i+1}: {response.status_code}")

        time.sleep(0.1)  # Small delay between requests

    print("   ⚠️  Warning: Did not hit rate limit")

def test_public_endpoints():
    """Test public endpoints (should work without auth)"""
    print("\n5. Testing public endpoints...")

    endpoints = ["/health", "/stats", "/api"]
    for endpoint in endpoints:
        response = requests.get(f"{BASE_URL}{endpoint}")
        assert response.status_code == 200, f"{endpoint} failed: {response.status_code}"
        print(f"   ✅ {endpoint}: {response.status_code}")

if __name__ == "__main__":
    print("="*60)
    print("API Authentication & Rate Limiting Tests")
    print("="*60)

    if not API_KEY or API_KEY == "test-key":
        print("\n⚠️  Warning: No API_KEY environment variable set")
        print("Set it with: export API_KEY='your-key'\n")

    try:
        test_no_auth()
        test_invalid_auth()
        test_valid_auth()
        test_rate_limit()
        test_public_endpoints()

        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60)

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
```

**Run tests:**
```bash
export API_KEY="your-actual-api-key"
python test_api_auth.py
```

---

## Security Best Practices

### 1. API Key Generation

**Generate strong keys:**
```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32

# Example output:
# jK8xL2mN4pQ6rS8tU9vW0xY1zA2bC3dE4fG5hI6jK7lM8nO9pQ0rS1t
```

**Minimum requirements:**
- At least 32 characters
- Mix of letters, numbers, special characters
- Cryptographically random

### 2. Key Storage

**DO:**
- ✅ Store in environment variables
- ✅ Use secret management (AWS Secrets Manager, HashiCorp Vault)
- ✅ Rotate keys regularly (monthly/quarterly)
- ✅ Use different keys for dev/staging/production

**DON'T:**
- ❌ Hardcode in source code
- ❌ Commit to git
- ❌ Share in Slack/email
- ❌ Include in client-side code (frontend)

### 3. Frontend Key Handling

**WRONG (exposes key to users):**
```javascript
// ❌ DON'T DO THIS
const API_KEY = "abc123def456";  // Visible in browser!
```

**CORRECT (server-side only):**
```javascript
// ✅ In Next.js server component or API route
// File: app/api/insert/route.ts
export async function POST(request: Request) {
  const API_KEY = process.env.API_KEY;  // Server-side only

  // Make authenticated request to backend
  const response = await fetch('https://api.example.com/insert', {
    headers: { 'X-API-Key': API_KEY }
  });

  return response;
}
```

### 4. Monitoring & Alerts

**Track:**
- Failed authentication attempts
- Rate limit hits
- Unusual usage patterns
- API key usage by endpoint

**Alert on:**
- Multiple 401 errors (possible attack)
- Sudden spike in usage (possible leak)
- Rate limits constantly hit (need increase)

### 5. Key Rotation

**Process:**
1. Generate new API key
2. Update environment variable on server
3. Test with new key
4. Update all clients
5. Monitor for 401 errors
6. Revoke old key after grace period

**Automation:**
```bash
#!/bin/bash
# rotate_api_key.sh

# Generate new key
NEW_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

# Update on Render (example)
render env set API_KEY="$NEW_KEY" --service=your-service

# Save to password manager
echo "New API key: $NEW_KEY" | pbcopy

echo "✅ Key rotated. Update clients now!"
```

---

## Backward Compatibility

### Optional Authentication

The auth system is **backward compatible**:

```python
# If API_KEY environment variable is NOT set:
# - All requests are allowed
# - No authentication required

# If API_KEY environment variable IS set:
# - Authentication required on protected endpoints
# - 401 error if key missing/invalid
```

**This allows:**
- Development without auth (local testing)
- Gradual rollout (add API_KEY when ready)
- Easier debugging (disable temporarily)

**For production:**
```bash
# ALWAYS set API_KEY in production!
export API_KEY="strong-random-key-here"
```

---

## Summary

### Key Points

1. **API Key Authentication** protects `/insert`, `/search`, `/chat`
2. **X-API-Key header** required for protected endpoints
3. **Rate limiting** prevents abuse (10-30 req/min)
4. **401 Unauthorized** returned for invalid/missing keys
5. **429 Too Many Requests** returned when rate limited
6. **Backward compatible** - optional authentication mode

### Quick Reference

**Generate API Key:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Set Environment Variable:**
```bash
export API_KEY="your-generated-key"
```

**Make Authenticated Request:**
```bash
curl -X POST https://api.example.com/insert \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content": "test"}'
```

**Check Response:**
- 200 = Success
- 401 = Authentication failed
- 429 = Rate limited
- 503 = Service unavailable

---

**Last Updated:** 2025-11-19
**Version:** 1.0
**Status:** Production Ready
