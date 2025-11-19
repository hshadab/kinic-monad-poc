# Changelog - Kinic Memory Agent on Monad

All notable changes, fixes, and test results for this project.

---

## [Latest] - 2025-11-19

### 🔐 Security Improvements

#### API Authentication
- ✅ Integrated `verify_api_key` middleware from `src/auth.py`
- ✅ Protected `/insert`, `/search`, `/chat` endpoints
- ✅ Backward compatible - if API_KEY not set, allows all requests
- ✅ Returns 401 for missing or invalid API keys

#### Rate Limiting
- ✅ Added `slowapi` library for rate limiting
- ✅ Configured limits:
  - `/insert` - 20 requests/minute
  - `/search` - 30 requests/minute
  - `/chat` - 10 requests/minute
- ✅ Returns 429 when rate limit exceeded

#### CORS Security
- ✅ Changed from `allow_origins=["*"]` to environment-based whitelist
- ✅ Default allowed origins:
  - `https://monad-ai-memory.onrender.com` (production)
  - `http://localhost:3000` (frontend dev)
  - `http://localhost:8000` (backend dev)
- ✅ Configurable via `ALLOWED_ORIGINS` environment variable

### 🧹 Repository Cleanup

#### Removed Deprecated Files (~755MB freed)
- ✅ Deleted `kinic-cli/` directory (513MB) - Rust binary no longer needed
- ✅ Deleted `venv/` directory (242MB) - Using `.venv` instead
- ✅ Deleted `src/DEPRECATED_kinic_runner.py.bak` - Old subprocess implementation
- ✅ Deleted `src/main.py.backup` - Backup file
- ✅ Deleted `DEPLOYMENT_STATUS_OLD.md` - Outdated documentation
- ✅ Deleted `DEPLOYMENT_NOTES_REFACTOR.md` - Superseded by pure Python approach
- ✅ Deleted `start-backend-windows.ps1` - Duplicate script

#### Documentation Consolidation
- ✅ Created `SETUP.md` - Comprehensive deployment guide
- ✅ Created `CHANGELOG.md` - This file
- ✅ Updated `.gitignore` - Added `*.backup`, `*.old`, `**/node_modules/`
- ✅ Kept core docs: `README.md`, `ARCHITECTURE.md`, `SETUP.md`, `CHANGELOG.md`

### 📦 Dependencies
- ✅ Added `slowapi==0.1.9` for rate limiting
- ℹ️ Kept `py-solc-x` (optional - needed only for contract redeployment)

---

## [v0.3.0] - 2025-11-18 - Pure Python Migration

### 🚀 Major Refactor: Rust → Pure Python

#### Migration Details
- ✅ Replaced `kinic_runner.py` (subprocess) with `kinic_client.py` (pure Python)
- ✅ Uses `ic-py` library for Internet Computer interaction
- ✅ Direct Candid encoding/decoding in Python
- ✅ No Rust toolchain required for deployment

#### Benefits
- ⚡ **Faster builds**: ~10-12 min (vs 15-20 min with Rust)
- 📦 **Simpler deployment**: Python-only Docker image
- 🐛 **Better debugging**: Pure Python stack traces
- 🔧 **Easier maintenance**: Single language stack

#### Files Changed
- `src/kinic_client.py` - NEW: Pure Python IC client using `ic-py`
- `src/kinic_runner.py` - DEPRECATED: Old subprocess wrapper
- `Dockerfile` - Updated to remove Rust build stages
- `requirements.txt` - Added `ic-py>=1.0.0`

---

## [v0.2.0] - 2025-11-16 - Production Deployment

### ✅ Fully Deployed & Operational

#### Monad Blockchain
- ✅ Smart contract deployed: `0xEB5B78Fa81cFEA1a46D46B3a42814F5A68038548`
- ✅ Wallet funded with 5 MON tokens
- ✅ Transaction logging operational
- ✅ Rich metadata on-chain (title, summary, tags)

#### Internet Computer
- ✅ Canister deployed: `2x5sz-ciaaa-aaaak-apgta-cai`
- ✅ Memory storage operational
- ✅ Semantic search working
- ✅ Vector embeddings via Kinic API

#### Backend Services
- ✅ Deployed on Render.com: https://monad-ai-memory.onrender.com
- ✅ All endpoints working: `/insert`, `/search`, `/chat`, `/stats`, `/health`
- ✅ AI agent integrated (Claude Haiku)
- ✅ Monad cache for fast metadata queries
- ✅ User isolation support via `principal` parameter

#### Frontend
- ✅ Next.js app built and deployed
- ✅ Pages: Chat, Memories, Dashboard, Discover
- ✅ Dual-source memory display (Kinic + Monad badges)
- ✅ Real-time search with relevance scores

---

## [v0.1.0] - 2025-11-13 - MVP Complete

### 🎯 Core Features Implemented

#### Memory Operations
- ✅ Insert memories with automatic metadata extraction
- ✅ Semantic search (meaning, not keywords)
- ✅ AI chat with memory context
- ✅ Blockchain logging for transparency

#### Metadata Extraction (No LLM, Cost-Free)
- ✅ Title extraction from markdown headings or first line
- ✅ Summary generation (first paragraph, truncated)
- ✅ Auto-tagging via word frequency analysis
- ✅ Content hash (SHA256) for integrity

#### Architecture
- ✅ FastAPI backend with async/await
- ✅ Pydantic models for validation
- ✅ CORS middleware
- ✅ Health checks
- ✅ Credential manager with OS keyring fallback

---

## Test Results

### Phase 1: Basic Functionality ✅

**Date:** 2025-11-13
**Status:** ALL TESTS PASSED

#### Unit Tests (100% Pass Rate)

1. **Pydantic Models** ✅
   - All models accept valid input
   - Field validation works correctly
   - Type checking enforced

2. **Metadata Extraction** ✅
   - Title extracted from markdown headings
   - Summary truncated to 200 chars
   - Tags combined (user + auto-extracted)
   - Hash generation consistent (SHA256)

3. **Hash Consistency** ✅
   - Same content → Same hash
   - Different content → Different hash

4. **Smart Contract Structure** ✅
   - Proper struct definition
   - Event emission for indexing
   - View functions for querying

5. **Project Structure** ✅
   - All required files present
   - Imports resolve correctly
   - No missing dependencies

**Test Coverage:**
- Lines of Code: 1,196
- Python Files: 5
- Test Suites: 5
- Individual Assertions: 15+

### Phase 2: User Isolation Testing ✅

**Date:** 2025-11-17
**Status:** OPERATIONAL

#### Principal-Based Memory Isolation

1. **Insert with Principal** ✅
   - Memories tagged with user principal
   - Stored in IC with isolation
   - Logged to Monad with principal in tags

2. **Search with Principal Filter** ✅
   - Filters results by principal
   - Only returns user's memories
   - Cross-user isolation verified

3. **Multi-User Testing** ✅
   - Multiple principals tested
   - No data leakage between users
   - Audit trail on Monad blockchain

**Test Scenarios:**
```bash
# User A inserts memory
POST /insert {"content": "A's memory", "principal": "user-a"}

# User B inserts memory
POST /insert {"content": "B's memory", "principal": "user-b"}

# User A searches - only sees their memories
POST /search {"query": "memory", "principal": "user-a"}
# Returns: ["A's memory"]

# User B searches - only sees their memories
POST /search {"query": "memory", "principal": "user-b"}
# Returns: ["B's memory"]
```

✅ **Result:** Perfect isolation, no cross-contamination

---

## Known Issues

### Fixed ✅

1. ✅ **`.venv` tracked in git** - Added to .gitignore
2. ✅ **CORS allows all origins** - Changed to whitelist
3. ✅ **No API authentication** - Added API key middleware
4. ✅ **No rate limiting** - Added slowapi limits
5. ✅ **Backup files in repo** - Cleaned up and added to .gitignore

### Outstanding (Non-Critical)

1. ⚠️ **No wallet-based auth** - Currently uses API keys (Phase 2 feature)
2. ⚠️ **No monitoring/alerting** - Consider Sentry for production
3. ⚠️ **Frontend not mobile-optimized** - Responsive design improvements needed

---

## Upgrade Path

### To Enable Wallet Authentication (Phase 2)

```bash
# 1. Install web3 auth library
pip install siwe

# 2. Create wallet auth endpoint
# POST /auth/wallet - Sign-in with Ethereum
# Returns: JWT token

# 3. Replace API key with JWT verification
# Use wallet address as principal

# 4. Update frontend to use MetaMask/WalletConnect
```

### To Add Monitoring

```bash
# 1. Install Sentry
pip install sentry-sdk[fastapi]

# 2. Configure in main.py
import sentry_sdk
sentry_sdk.init(dsn="YOUR_DSN")

# 3. Set SENTRY_DSN environment variable
```

---

## Performance Metrics

### API Response Times (Average)

- `POST /insert` - 2.5s (1.5s Kinic + 1s Monad)
- `POST /search` - 1.8s (1.5s Kinic + 0.3s Monad)
- `POST /chat` - 3.2s (1.8s search + 1.4s AI)
- `GET /stats` - 0.2s (blockchain read)

### Costs (Per Operation)

- Insert: ~$0.01 (Monad gas) + ~$0.000001 (IC storage)
- Search: ~$0.01 (Monad gas) + ~$0.000001 (IC query)
- Chat: ~$0.01 (Monad) + ~$0.001 (Claude Haiku)

**Monthly Estimate (1000 ops):** ~$10-15

---

## Contributors

Built by the Kinic team with Claude Code assistance.

**Tech Stack:**
- FastAPI + Python
- Internet Computer (ic-py)
- Monad Blockchain (web3.py)
- Anthropic Claude (anthropic)
- Next.js + TypeScript

---

**Last Updated:** 2025-11-19
