# Setup Guide - Kinic Memory Agent on Monad

Complete guide for deploying and configuring the Kinic Memory Agent.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Credential Configuration](#credential-configuration)
- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [API Authentication](#api-authentication)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Tools
- **Python 3.12+** - Pure Python implementation (no Rust needed!)
- **Node.js 18+** - For frontend build
- **Git** - Version control

### Required Accounts & Keys
1. **Monad Wallet** - Private key with MON tokens for gas
2. **Internet Computer Identity** - PEM format private key
3. **Anthropic API Key** - For Claude AI integration
4. **Monad RPC Endpoint** - API key from Monad infrastructure

---

## Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/kinic-monad-poc
cd kinic-monad-poc
```

### 2. Install Python Dependencies

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies (Optional)

```bash
cd frontend
npm install
npm run build
cd ..
```

---

## Credential Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Monad Blockchain Configuration
MONAD_RPC_URL=https://rpc-mainnet.monadinfra.com/rpc/YOUR_API_KEY
MONAD_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
MONAD_CONTRACT_ADDRESS=0xYOUR_CONTRACT_ADDRESS

# Internet Computer Configuration
KINIC_MEMORY_ID=your-canister-id-here
IC_IDENTITY_PEM=-----BEGIN EC PRIVATE KEY-----
YOUR_PEM_KEY_HERE
-----END EC PRIVATE KEY-----

# AI Configuration
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE

# API Security (IMPORTANT!)
API_KEY=your-secret-api-key-here

# CORS Configuration (comma-separated)
ALLOWED_ORIGINS=https://your-domain.com,http://localhost:3000
```

### Obtaining Credentials

#### 1. Monad Wallet & RPC

```bash
# Generate new wallet (or use existing)
python scripts/generate_wallet.py

# Get RPC endpoint from Monad
# Visit: https://monad.xyz or contact Monad team
```

#### 2. Internet Computer Identity

**Option A: Using dfx (recommended)**
```bash
dfx identity export default > identity.pem
# Copy the PEM content to IC_IDENTITY_PEM in .env
```

**Option B: Generate new identity**
```bash
# Use IC SDK to create new identity
dfx identity new kinic_agent
dfx identity export kinic_agent > identity.pem
```

#### 3. Deploy Monad Smart Contract

```bash
# Make sure you have MON tokens in your wallet
export MONAD_PRIVATE_KEY=0xYOUR_KEY
export MONAD_RPC_URL=https://rpc-mainnet.monadinfra.com/rpc/YOUR_API_KEY

# Deploy contract
python contracts/deploy.py

# Copy the contract address to .env
```

#### 4. Anthropic API Key

```bash
# Get API key from https://console.anthropic.com
# Add to .env as ANTHROPIC_API_KEY
```

---

## Local Development

### Running the Backend

```bash
# Activate virtual environment
source .venv/bin/activate

# Run with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Access the API at: http://localhost:8000

### Running the Frontend (Optional)

```bash
cd frontend
npm run dev
```

Access the frontend at: http://localhost:3000

### Testing

```bash
# Run basic tests
python test_basic.py

# Test without blockchain (offline)
python test_without_blockchain.py

# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/stats
```

---

## Production Deployment

### Deploy to Render.com

#### 1. Push to GitHub

```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

#### 2. Create Render Web Service

1. Go to https://render.com
2. Create new **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Environment**: Docker
   - **Branch**: main
   - **Build Command**: (automatic from Dockerfile)
   - **Start Command**: (automatic from Dockerfile)

#### 3. Set Environment Variables

Add all variables from your `.env` file to Render:

```
MONAD_RPC_URL=...
MONAD_PRIVATE_KEY=...
MONAD_CONTRACT_ADDRESS=...
KINIC_MEMORY_ID=...
IC_IDENTITY_PEM=...  (full PEM including BEGIN/END lines)
ANTHROPIC_API_KEY=...
API_KEY=...  (generate strong random key!)
ALLOWED_ORIGINS=https://your-app.onrender.com
```

**IMPORTANT:** Use strong, unique API_KEY for production!

```bash
# Generate secure API key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 4. Deploy

Click "Create Web Service" - Render will:
1. Build Docker image (~10-12 minutes)
2. Deploy container
3. Assign URL: `https://your-app.onrender.com`

---

## API Authentication

### How Authentication Works

The API uses **API Key authentication** via the `X-API-Key` header.

- If `API_KEY` environment variable is set, all requests require authentication
- If not set, API runs in open mode (NOT recommended for production)

### Using the API with Authentication

```bash
# Set your API key
export API_KEY="your-secret-key"

# Make authenticated requests
curl -X POST https://your-app.onrender.com/insert \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key" \
  -d '{"content": "Test memory", "user_tags": "test"}'
```

### Rate Limits

Protected endpoints have rate limits:
- `/insert` - 20 requests/minute
- `/search` - 30 requests/minute
- `/chat` - 10 requests/minute

Exceeding limits returns `429 Too Many Requests`.

---

## Troubleshooting

### Common Issues

#### "Services not initialized" Error

**Cause:** Environment variables not loaded or invalid credentials

**Fix:**
```bash
# Check environment variables are set
env | grep -E "MONAD|KINIC|ANTHROPIC"

# Verify .env file exists and has correct format
cat .env

# Check logs for specific credential errors
```

#### "IC connection failed"

**Cause:** Invalid IC_IDENTITY_PEM format

**Fix:**
```bash
# Ensure PEM has proper line breaks
# Should look like:
# IC_IDENTITY_PEM=-----BEGIN EC PRIVATE KEY-----
# MHQCAQEEIC...
# ...
# -----END EC PRIVATE KEY-----

# Test PEM parsing
python -c "
from src.kinic_client import KinicClient
import os
pem = os.getenv('IC_IDENTITY_PEM')
print('PEM length:', len(pem))
print('Has BEGIN:', 'BEGIN' in pem)
print('Has END:', 'END' in pem)
"
```

#### "Monad transaction failed"

**Cause:** Insufficient gas or invalid private key

**Fix:**
```bash
# Check wallet balance
python -c "
from web3 import Web3
from src.monad import MonadLogger
import os

monad = MonadLogger(
    os.getenv('MONAD_RPC_URL'),
    os.getenv('MONAD_PRIVATE_KEY'),
    os.getenv('MONAD_CONTRACT_ADDRESS')
)
balance = monad.w3.eth.get_balance(monad.account.address)
print(f'Balance: {Web3.from_wei(balance, \"ether\")} MON')
"
```

#### Rate Limit Exceeded

**Cause:** Too many requests in short time

**Fix:**
- Wait 60 seconds before retrying
- Implement exponential backoff in your client
- Request rate limit increase for production use

#### CORS Errors in Browser

**Cause:** Frontend domain not in ALLOWED_ORIGINS

**Fix:**
```bash
# Update ALLOWED_ORIGINS environment variable
ALLOWED_ORIGINS=https://your-frontend.com,http://localhost:3000

# Restart server
```

---

## Platform-Specific Notes

### Windows Setup

```powershell
# Use PowerShell to set environment variables
$env:MONAD_RPC_URL="https://..."
$env:MONAD_PRIVATE_KEY="0x..."

# Run backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn src.main:app --reload
```

### Linux/WSL Setup

```bash
# Standard Unix setup works
source .venv/bin/activate
uvicorn src.main:app --reload
```

---

## Security Best Practices

1. **Never commit .env files** - Already in .gitignore
2. **Rotate API keys regularly** - Especially after any exposure
3. **Use strong API_KEY** - Generate with `secrets.token_urlsafe(32)`
4. **Restrict CORS origins** - Only allow your domains
5. **Monitor API usage** - Check for unusual patterns
6. **Enable rate limiting** - Already configured in main.py

---

## Next Steps

After successful deployment:

1. **Test all endpoints** - Use `curl` or Postman
2. **Monitor logs** - Check Render dashboard
3. **Set up monitoring** - Consider Sentry for error tracking
4. **Configure custom domain** - See Render docs
5. **Backup credentials** - Store securely offline

---

**Deployment Status:** ✅ Production Ready

**Support:** Open an issue on GitHub for help

**Last Updated:** 2025-11-19
