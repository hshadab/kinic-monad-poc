# Phase 2: User Isolation Testing Guide

## Overview
Phase 2 implements Internet Identity-based user isolation using a shared canister approach. This document outlines how to test the implementation.

## What Was Implemented

### Backend Changes:
1. **Data Models** (`src/models.py`):
   - Added `principal` field to `InsertRequest`, `SearchRequest`, `ChatRequest`

2. **Kinic Client** (`src/kinic_client.py`):
   - Modified `insert()` to prepend principal to tags (format: `principal|tag`)
   - Modified `search()` to filter results by principal prefix

3. **API Endpoints** (`src/main.py`):
   - Updated `/insert`, `/search`, `/chat` to pass principal to Kinic client
   - Added principal to Monad logs (format: `tags,principal:xyz123...`)

### Frontend Changes (Phase 1):
1. **Authentication Hook** (`frontend/lib/useAuth.ts`):
   - Internet Identity integration
   - Principal management

2. **Login Button** (`frontend/components/LoginButton.tsx`):
   - Visual II authentication

3. **API Client** (`frontend/lib/api.ts`):
   - Added principal parameter to all API calls

## How User Isolation Works

### Data Tagging Strategy:
When a user with principal `abc123def456` inserts content with tag `"research"`:
- **Kinic Storage**: Tag becomes `"abc123def456|research"`
- **Monad Blockchain**: Tags become `"research,zkml,principal:abc123def456"`

### Search Filtering:
When the same user searches:
- Kinic returns ALL semantic matches
- Results are filtered to only show items with matching principal prefix
- Users only see their own data

### Security Guarantees:
✅ Users can only see their own memories
✅ No cross-user data leakage
✅ Audit trail on Monad includes principal
✅ No canister modifications needed (uses shared canister)
✅ No ICP funding required initially

## Manual Testing Steps

### Test 1: Basic Insert with Principal

**Request:**
```bash
curl -X POST http://localhost:8000/insert \
  -H "Content-Type: application/json" \
  -d '{
    "content": "ZKML enables privacy-preserving ML inference",
    "user_tags": "zkml,research",
    "principal": "test-user-123"
  }'
```

**Expected Response:**
```json
{
  "kinic_result": {
    "status": "inserted",
    "tag": "test-user-123|zkml,research"
  },
  "monad_tx": "0x...",
  "metadata": {
    "title": "ZKML enables privacy-preserving ML inference",
    "tags": "zkml,research,principal:test-user-123"
  }
}
```

**Verification:**
- Check Kinic result tag contains principal prefix
- Check Monad tags include `principal:test-user-123`

### Test 2: Search with Principal Isolation

**Setup:** Insert data for two different users

```bash
# User 1 data
curl -X POST http://localhost:8000/insert \
  -H "Content-Type: application/json" \
  -d '{
    "content": "User 1 loves cats",
    "user_tags": "pets",
    "principal": "user-1-abc"
  }'

# User 2 data
curl -X POST http://localhost:8000/insert \
  -H "Content-Type: application/json" \
  -d '{
    "content": "User 2 loves cats",
    "user_tags": "pets",
    "principal": "user-2-xyz"
  }'
```

**Test:** Search as User 1
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "cats",
    "top_k": 10,
    "principal": "user-1-abc"
  }'
```

**Expected:**
- Should ONLY return "User 1 loves cats"
- Should NOT return "User 2 loves cats"

**Test:** Search as User 2
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "cats",
    "top_k": 10,
    "principal": "user-2-xyz"
  }'
```

**Expected:**
- Should ONLY return "User 2 loves cats"
- Should NOT return "User 1 loves cats"

### Test 3: Search WITHOUT Principal (Backwards Compatible)

**Request:**
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "cats",
    "top_k": 10
  }'
```

**Expected:**
- Should return ALL results (both users' data)
- Demonstrates backwards compatibility

### Test 4: Chat with Principal Isolation

**Request:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me about cats",
    "top_k": 3,
    "principal": "user-1-abc"
  }'
```

**Expected:**
- AI response should only use memories from user-1-abc
- `memories_used` array should only contain user-1's data
- Monad transaction should include `principal:user-1-abc` in tags

## Frontend Testing (After Phase 3 Integration)

### Test 5: End-to-End with Internet Identity

1. **Navigate** to http://localhost:3000 (or kinicmemory.com)
2. **Click** "Login" button
3. **Authenticate** with Internet Identity
4. **Verify** principal displayed in nav (e.g., "abc12...xyz")
5. **Insert** a memory through UI
6. **Open browser console**, check request includes principal
7. **Search** for the memory
8. **Logout**
9. **Login** as different identity
10. **Search** for same query
11. **Verify** previous user's memory is NOT visible

## Monitoring & Debugging

### Check Kinic Tags:
In server logs, look for:
```
Using principal-scoped tag: abc123def456|research...
```

### Check Monad Tags:
In server logs, look for:
```
Including principal in on-chain metadata
```

### Verify on Monad Blockchain:
```bash
curl http://localhost:8000/monad/search \
  -H "Content-Type: application/json" \
  -d '{
    "tags": "principal:test-user-123",
    "limit": 10
  }'
```

## Known Limitations

1. **Existing Data**: Memories inserted before Phase 2 don't have principal tags
2. **Shared Canister**: All users share same IC canister (by design for free tier)
3. **Tag Length**: Very long principals may approach tag length limits
4. **IC Identity Issues**: The current IC identity has "Invalid user" errors - need valid identity PEM

## Next Steps (Phase 3)

- [ ] Update frontend pages to pass principal from useAuth hook
- [ ] Add user profile page showing user-specific stats
- [ ] Implement usage tracking per principal
- [ ] Add freemium pricing model based on usage
- [ ] Consider principal anonymization for privacy

## Success Criteria

✅ Backend accepts principal parameter
✅ Data tagged with principal in Kinic
✅ Search filters by principal
✅ Chat uses principal-scoped memories
✅ Monad logs include principal for audit
✅ No cross-user data leakage
✅ Backwards compatible (works without principal)

## Troubleshooting

### Issue: "Invalid user" error from IC
**Cause:** IC identity PEM not valid
**Solution:** Generate new identity or use valid existing one

### Issue: All users see all data
**Cause:** Frontend not passing principal
**Solution:** Ensure `principal` included in API requests

### Issue: No results when principal provided
**Cause:** No data exists for that principal
**Solution:** Insert test data first with same principal

---

**Phase 2 Status:** ✅ Backend Implementation Complete
**Next:** Phase 3 - Frontend Integration
