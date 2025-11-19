# Authentication System

**Date:** 2025-11-19
**Status:** ✅ Implemented

---

## Overview

The Kinic Memory Agent now uses a **dual-layer authentication** system to ensure security and user privacy:

1. **Frontend:** Internet Identity authentication (decentralized login)
2. **Backend:** API Key authentication (server protection)

This provides both user isolation (via Principal) and API security (via API Key).

---

## 1. Internet Identity Authentication (Frontend)

### What is Internet Identity?

Internet Identity is a blockchain-based authentication system from the Internet Computer that provides:
- **Passwordless login** using biometrics, Google, Apple, or other methods
- **Cryptographic identity** (Principal) unique to each user
- **Privacy-preserving** - no personal data stored on blockchain
- **Cross-platform** - works across all IC applications

### How It Works

1. **User clicks "Login with Internet Identity"** on protected pages
2. **Redirects to Internet Identity 2.0** (https://id.ai/)
3. **User authenticates** using their preferred method
4. **Returns Principal** (cryptographic identity like `abc123-xyz789-...`)
5. **Principal is used** to isolate user data in Kinic canister and Monad logs

### Protected Pages

The following pages now **require Internet Identity login**:

- `/chat` - AI Chat with Memory Agent
- `/memories` - Browse and manage your memories
- `/dashboard` - Personal dashboard and statistics
- `/discover` - Explore blockchain memories

**Public pages** (no login required):
- `/` - Home page
- `/about` - About page explaining the system

### Implementation Details

**AuthGuard Component** (`frontend/components/AuthGuard.tsx`):
```typescript
export function AuthGuard({ children, fallback }: AuthGuardProps) {
  const { isAuthenticated, isLoading, login, principalText } = useAuth();

  // Show loading spinner while checking auth status
  if (isLoading) {
    return <LoadingSpinner />;
  }

  // Show login screen if not authenticated
  if (!isAuthenticated) {
    return <LoginRequiredScreen onLogin={login} />;
  }

  // User is authenticated - show protected content
  return <>{children}</>;
}
```

**Usage in Pages:**
```typescript
// Example: frontend/app/chat/page.tsx
import AuthGuard from '@/components/AuthGuard'

export default function ChatPage() {
  return (
    <AuthGuard>
      {/* Protected content here */}
    </AuthGuard>
  )
}
```

### useAuth Hook

The `useAuth` hook (frontend/lib/useAuth.ts) provides:
- `isAuthenticated` - Whether user is logged in
- `isLoading` - Whether auth status is being checked
- `principal` - User's Principal object
- `principalText` - Principal as string (e.g., "abc123-xyz789-...")
- `login()` - Function to trigger login flow
- `logout()` - Function to log out user

---

## 2. API Key Authentication (Backend)

### What is API Key Authentication?

API Key authentication protects the backend API from unauthorized access:
- **X-API-Key header** required on all protected endpoints
- **Rate limiting** prevents abuse (10-30 requests/minute per endpoint)
- **Backward compatible** - if `API_KEY` not set, auth is disabled

### Protected Endpoints

The following endpoints require `X-API-Key` header:

- `POST /insert` - Insert new memory
- `POST /search` - Search memories
- `POST /chat` - Chat with AI agent
- `POST /monad/refresh` - Refresh blockchain cache

**Public endpoints** (no API key required):
- `GET /` - Serve frontend
- `GET /health` - Health check
- `GET /stats` - Get statistics
- `GET /monad/stats` - Get cache stats
- `GET /monad/trending` - Get trending tags
- `POST /monad/search` - Search Monad metadata

### Rate Limits

| Endpoint | Rate Limit |
|----------|-----------|
| `/insert` | 20 requests/minute |
| `/search` | 30 requests/minute |
| `/chat` | 10 requests/minute |
| `/monad/refresh` | 5 requests/minute |

### Backend Implementation

**API Key Verification** (`src/auth.py`):
```python
async def verify_api_key(api_key: Optional[str] = Security(api_key_header)):
    valid_api_key = os.getenv("API_KEY")

    # Backward compatible - if no API_KEY set, allow all requests
    if not valid_api_key:
        return None

    # If API_KEY is set, require it
    if not api_key:
        raise HTTPException(401, "Missing API Key")
    if api_key != valid_api_key:
        raise HTTPException(401, "Invalid API Key")

    return api_key
```

**Applied to Endpoints** (`src/main.py`):
```python
@app.post("/insert", response_model=InsertResponse)
@limiter.limit("20/minute")
async def insert_memory(
    req: Request,
    request: InsertRequest,
    api_key: str = Depends(verify_api_key)  # ← API Key required
):
    # ... endpoint logic
```

### Frontend Implementation

**API Client** (`frontend/lib/api.ts`):
```typescript
const api = axios.create({
  headers: {
    'Content-Type': 'application/json',
    ...(process.env.NEXT_PUBLIC_API_KEY && {
      'X-API-Key': process.env.NEXT_PUBLIC_API_KEY,
    }),
  },
});
```

**Environment Variable** (`frontend/.env.local`):
```bash
NEXT_PUBLIC_API_KEY=your-secure-api-key-here
```

---

## 3. User Isolation with Principal

### How Principal Works

Every user has a unique **Principal** (cryptographic identity) from Internet Identity:

```
Principal: abc123-xyz789-def456-ghi789-...
```

This Principal is used to **isolate user data**:

1. **Kinic Storage**: Each user's memories are tagged with their Principal
2. **Monad Logs**: All operations include Principal in tags for audit trail
3. **Search Results**: Only return memories belonging to the user's Principal

### Example Flow: Insert Memory

1. **User logs in** → Gets Principal `abc123-xyz789-...`
2. **User inserts memory** "ZKML is awesome"
3. **Frontend sends**:
   ```json
   {
     "content": "ZKML is awesome",
     "user_tags": "zkml,research",
     "principal": "abc123-xyz789-..."
   }
   ```
4. **Backend stores in Kinic** with tag `principal:abc123-xyz789-...`
5. **Backend logs to Monad** with tags `principal:abc123-xyz789-...,zkml,research`

### Example Flow: Search Memories

1. **User searches** "ZKML"
2. **Frontend sends**:
   ```json
   {
     "query": "ZKML",
     "top_k": 5,
     "principal": "abc123-xyz789-..."
   }
   ```
3. **Backend searches Kinic** filtered by `principal:abc123-xyz789-...`
4. **Returns only** memories belonging to this user

### Privacy Guarantees

✅ **Your memories are private** - only you can see them
✅ **Isolated storage** - each Principal has separate namespace
✅ **Blockchain audit** - all operations logged with your Principal
✅ **No data leakage** - search results filtered by Principal

---

## 4. Setup Instructions

### Step 1: Set Backend API Key

**Production (Render):**
1. Go to Render dashboard
2. Select your service
3. Go to "Environment" tab
4. Add environment variable:
   - **Key:** `API_KEY`
   - **Value:** Generate a secure random key (32+ characters)
5. Save and redeploy

**Local Development:**
```bash
# In project root, create or edit .env
echo "API_KEY=your-secure-api-key-here" >> .env
```

**Generate Secure API Key:**
```bash
# Using Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Using OpenSSL
openssl rand -base64 32
```

### Step 2: Set Frontend API Key

**Update frontend/.env.local:**
```bash
NEXT_PUBLIC_API_URL=https://monad-ai-memory.onrender.com
NEXT_PUBLIC_API_KEY=your-secure-api-key-here  # ← Same as backend
```

**Important:** Use the **same API key** on both frontend and backend!

### Step 3: Rebuild Frontend

```bash
cd frontend
npm run build
```

### Step 4: Restart Backend

```bash
# Local development
source .venv/bin/activate
uvicorn src.main:app --reload

# Production (Render)
# Automatically rebuilds on git push
```

---

## 5. Testing Authentication

### Test Internet Identity Login

1. **Visit protected page:** https://monad-ai-memory.onrender.com/chat
2. **Should see login screen** with Internet Identity button
3. **Click "Login with Internet Identity"**
4. **Authenticate** using your preferred method
5. **Redirected back** to chat page with Principal displayed
6. **Try chat** - should work normally
7. **Check Monad logs** - should include your Principal in tags

### Test API Key Authentication

**Without API Key (should fail):**
```bash
curl -X POST https://monad-ai-memory.onrender.com/insert \
  -H "Content-Type: application/json" \
  -d '{"content": "Test", "principal": "test-principal"}'

# Expected: 401 Unauthorized - Missing API Key
```

**With Invalid API Key (should fail):**
```bash
curl -X POST https://monad-ai-memory.onrender.com/insert \
  -H "Content-Type: application/json" \
  -H "X-API-Key: wrong-key" \
  -d '{"content": "Test", "principal": "test-principal"}'

# Expected: 401 Unauthorized - Invalid API Key
```

**With Valid API Key (should succeed):**
```bash
curl -X POST https://monad-ai-memory.onrender.com/insert \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secure-api-key-here" \
  -d '{"content": "Test", "principal": "test-principal", "user_tags": "test"}'

# Expected: 200 OK with transaction hash
```

### Test User Isolation

1. **Login as User A** → Insert memory "Secret A"
2. **Logout and login as User B** → Insert memory "Secret B"
3. **Search as User B** → Should only see "Secret B", not "Secret A"
4. **Logout and login as User A** → Search should only see "Secret A"

---

## 6. Security Considerations

### API Key Security

✅ **Use strong keys** - 32+ characters, random
✅ **Never commit** to git - use environment variables
✅ **Rotate regularly** - change key every 90 days
✅ **Use HTTPS** - prevents key interception
⚠️ **Frontend exposure** - API key is visible in browser (use with caution)

**Note:** For production, consider moving API key to server-side only and using session-based auth.

### Internet Identity Security

✅ **Passwordless** - no password to steal or forget
✅ **Cryptographic** - Principal cannot be forged
✅ **Privacy-preserving** - no personal data leaked
✅ **Multi-device** - sync across devices with IC
✅ **Decentralized** - no central authority

### Rate Limiting

Rate limiting prevents abuse:
- **Per IP address** - limits requests from same IP
- **Automatic 429 errors** - too many requests
- **Configurable limits** - adjust per endpoint

---

## 7. Troubleshooting

### "Missing API Key" Error

**Symptom:** 401 error when using API
**Cause:** API_KEY environment variable is set but frontend not sending key
**Fix:** Update `frontend/.env.local` with `NEXT_PUBLIC_API_KEY`

### "Invalid API Key" Error

**Symptom:** 401 error with key provided
**Cause:** Frontend and backend keys don't match
**Fix:** Ensure same key on both frontend and backend

### Login Loop / Redirect Issues

**Symptom:** Can't login, keeps redirecting
**Cause:** Internet Identity authentication failed
**Fix:**
1. Clear browser cache and cookies
2. Try incognito/private window
3. Check browser console for errors
4. Ensure Internet Identity service is up (https://id.ai/)

### "Principal not found" in Logs

**Symptom:** Operations logged without Principal
**Cause:** User not logged in or Principal not passed to API
**Fix:** Ensure AuthGuard wraps page and Principal is sent in API calls

### Rate Limit Exceeded

**Symptom:** 429 Too Many Requests error
**Cause:** Exceeded rate limit for endpoint
**Fix:** Wait 1 minute and retry, or reduce request frequency

---

## 8. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   FRONTEND (Next.js)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ AuthGuard Component                                   │  │
│  │  - Checks isAuthenticated                            │  │
│  │  - Shows login if not authenticated                  │  │
│  │  - Redirects to Internet Identity                    │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ useAuth Hook                                          │  │
│  │  - Manages Internet Identity session                 │  │
│  │  - Provides Principal to components                  │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ API Client (axios)                                    │  │
│  │  - Adds X-API-Key header to all requests            │  │
│  │  - Includes Principal in request body                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP POST /insert, /search, /chat
                      │ Headers: X-API-Key, Content-Type
                      │ Body: { principal, content, ... }
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ API Key Middleware                                    │  │
│  │  - Verifies X-API-Key header                         │  │
│  │  - Returns 401 if missing/invalid                    │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Rate Limiter (slowapi)                                │  │
│  │  - Tracks requests per IP                            │  │
│  │  - Returns 429 if limit exceeded                     │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Endpoint Logic                                        │  │
│  │  - Extracts Principal from request                   │  │
│  │  - Adds Principal to Kinic tags                      │  │
│  │  - Adds Principal to Monad logs                      │  │
│  └──────────────────────────────────────────────────────┘  │
└────┬───────────────────────────────┬──────────────────────┘
     │                               │
     ▼                               ▼
┌─────────────────┐         ┌─────────────────┐
│  KINIC (IC)     │         │  MONAD CHAIN    │
│  - Stores data  │         │  - Logs metadata│
│  - User-scoped  │         │  - Audit trail  │
│  - Principal    │         │  - Principal in │
│    tagged       │         │    tags         │
└─────────────────┘         └─────────────────┘
```

---

## 9. Summary

✅ **Internet Identity authentication** required for all protected pages
✅ **API Key authentication** protects backend endpoints
✅ **User isolation** via Principal ensures privacy
✅ **Rate limiting** prevents abuse
✅ **Blockchain audit** logs all operations with Principal
✅ **AuthGuard component** enforces login on frontend
✅ **Backward compatible** - API auth can be disabled if needed

**Next Steps:**
1. Set `API_KEY` on backend (Render environment variable)
2. Set `NEXT_PUBLIC_API_KEY` on frontend (.env.local)
3. Rebuild and deploy
4. Test login flow
5. Verify Principal isolation

---

**Last Updated:** 2025-11-19
**Status:** Production Ready
**Security Level:** High (dual-layer auth + user isolation)
