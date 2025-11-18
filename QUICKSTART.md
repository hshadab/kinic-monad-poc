# Quick Start Guide

Get your Kinic AI Memory Agent on Monad running!

## 🎉 Current Status

✅ **Already Deployed:**
- Internet Computer Canister: `2x5sz-ciaaa-aaaak-apgta-cai`
- AI Agent: Claude Haiku integrated
- Backend API: 100% complete and tested
- kinic-cli: Built and working on Windows

⏳ **Waiting for:**
- Monad tokens (contacted team)
- Smart contract deployment (when tokens arrive)

## Prerequisites

- Python 3.11+
- Anthropic API key (for Claude AI agent)
- Monad wallet with tokens
- IC identity PEM (for Internet Computer access)

**No longer needed:**
- ✅ ~~Rust nightly~~ - Pure Python implementation!
- ✅ ~~kinic-cli binary~~ - Uses ic-py library instead
- ✅ ~~DFX CLI~~ - PEM string is enough

## Quick Test (Current State)

Since the IC canister and AI agent are already deployed, you can test locally:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
# The .env already has:
# - KINIC_MEMORY_ID=2x5sz-ciaaa-aaaak-apgta-cai
# - ANTHROPIC_API_KEY=sk-ant-api03-...
# - IC identity credentials
# Missing: MONAD_CONTRACT_ADDRESS (pending deployment)

# 3. Run locally (without Monad logging for now)
uvicorn src.main:app --reload

# 4. Test AI chat with memory
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me about ZKML",
    "top_k": 3
  }'
```

## When Monad Tokens Arrive

Once the Monad team sends tokens to `0xDA9f4e4C9596a1dA338164FD22895D8C167C6Bd6`, complete the deployment:

```bash
# 1. Verify you have tokens
# Check balance at https://monad.xyz or using Web3

# 2. Deploy smart contract
cd /home/hshadab/monad/kinic-monad-poc
source venv/bin/activate
python contracts/deploy.py

# 3. Update .env with contract address
# The deploy script will show: "Contract deployed at: 0x..."
nano .env  # Add the MONAD_CONTRACT_ADDRESS

# 4. Test complete system
./scripts/test_local.sh
```

## Test IC Canister (Pure Python!)

No Rust binary needed! Test directly through the API:

```bash
# Test insert
curl -X POST http://localhost:8000/insert \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Test memory from quickstart",
    "user_tags": "test,quickstart"
  }'

# Test search
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "test memory",
    "top_k": 5
  }'
```

**Pure Python under the hood:**
- Uses `ic-py` library for IC communication
- Direct Candid encoding/decoding
- No subprocess calls
- Faster and simpler!

## Deploy to Render (After Monad Contract)

**Note:** Render deployment requires the Monad contract address. Complete this after tokens arrive and contract is deployed.

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Kinic AI Memory Agent on Monad"
   git remote add origin https://github.com/YOUR_USERNAME/kinic-monad-poc
   git push -u origin main
   ```

2. **Create Render Service**
   - Go to https://render.com/dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Render auto-detects Dockerfile
   - Click "Create Web Service"

3. **Set Environment Variables**

   In Render dashboard, add these secrets:

   | Key | Value | Current Status |
   |-----|-------|----------------|
   | `MONAD_CONTRACT_ADDRESS` | `0x...` | ⏳ After contract deployment |
   | `MONAD_PRIVATE_KEY` | `0x513c988...` | ✅ Already have |
   | `MONAD_RPC_URL` | `https://rpc-mainnet.monadinfra.com/rpc/...` | ✅ Already have |
   | `KINIC_MEMORY_ID` | `2x5sz-ciaaa-aaaak-apgta-cai` | ✅ Already deployed |
   | `IC_IDENTITY_NAME` | `kinic_local` | ✅ Already configured |
   | `IC_IDENTITY_PEM` | `-----BEGIN EC...` | ✅ Already have (from .env) |
   | `ANTHROPIC_API_KEY` | `sk-ant-api03-...` | ✅ Already have (from .env) |

4. **Deploy!**

   Render will automatically build and deploy your service.

5. **Test Live Endpoint**
   ```bash
   # Health check
   curl https://YOUR-APP.onrender.com/health

   # Chat with AI agent
   curl -X POST https://YOUR-APP.onrender.com/chat \
     -H "Content-Type: application/json" \
     -d '{
       "message": "What do you know about blockchain?",
       "top_k": 3
     }'

   # Insert memory
   curl -X POST https://YOUR-APP.onrender.com/insert \
     -H "Content-Type: application/json" \
     -d '{
       "content": "# Monad\nHigh-performance EVM blockchain with 10,000 TPS",
       "user_tags": "monad,blockchain"
     }'
   ```

## What You Built

🎉 **You now have:**

- ✅ An **AI-powered memory agent** using Claude Haiku
- ✅ Semantic memory storage on **Internet Computer** (via Kinic)
- ✅ Rich, human-readable metadata logged on **Monad blockchain**
- ✅ FastAPI service with **chat, insert, search** endpoints
- ✅ Provable audit trail of all memory operations
- ✅ Context-aware conversations with memory retrieval

**Current Status:**
- ✅ IC Canister: Deployed and tested (`2x5sz-ciaaa-aaaak-apgta-cai`)
- ✅ AI Agent: Integrated and working
- ⏳ Monad Contract: Waiting for tokens
- ⏳ Render Deployment: Ready when contract is deployed

## View On-Chain Data (After Contract Deployment)

Once the Monad contract is deployed, anyone can query to see what your agent learned:

```python
from web3 import Web3

# Use mainnet RPC
w3 = Web3(Web3.HTTPProvider("https://rpc-mainnet.monadinfra.com/rpc/YOUR_KEY"))
contract = w3.eth.contract(address="YOUR_CONTRACT_ADDRESS", abi=ABI)

# Get latest memory
total = contract.functions.getTotalMemories().call()
memory = contract.functions.getMemory(total - 1).call()

print(f"User: {memory[0]}")       # Who stored it
print(f"Title: {memory[2]}")      # Human-readable title
print(f"Summary: {memory[3]}")    # Content summary
print(f"Tags: {memory[4]}")       # Keywords
print(f"Hash: {memory[5]}")       # Content hash
print(f"Time: {memory[6]}")       # Timestamp
```

## API Examples

### 1. Chat with AI Agent (NEW!)

The AI agent retrieves relevant memories and uses them as context for responses:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is ZKML and how does it work?",
    "top_k": 3
  }'
```

Response:
```json
{
  "response": "ZKML (Zero-Knowledge Machine Learning) is a framework that enables verifiable ML inference. Jolt Atlas is one implementation that uses zero-knowledge proofs to verify that ML computations were performed correctly without revealing the model or data...",
  "memories_used": [
    {
      "text": "# ZKML Overview\nJolt Atlas enables verifiable ML inference",
      "score": 0.89,
      "tag": "zkml,test"
    }
  ],
  "num_memories": 1,
  "monad_tx": "0xabc123..."
}
```

### 2. Insert Memory

Store new knowledge with automatic metadata extraction:

```bash
curl -X POST http://localhost:8000/insert \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# ZKML\nJolt Atlas enables verifiable ML inference using zero-knowledge proofs",
    "user_tags": "zkml,research"
  }'
```

Response:
```json
{
  "kinic_result": {"status": "inserted"},
  "monad_tx": "0xabc123...",
  "metadata": {
    "title": "ZKML",
    "summary": "Jolt Atlas enables verifiable ML inference using zero-knowledge proofs",
    "tags": "zkml,research,jolt,atlas,enables",
    "content_hash": "0xdef456..."
  }
}
```

### 3. Search Memory

Semantic search (not just keywords):

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "how does zkml verification work?",
    "top_k": 5
  }'
```

Response:
```json
{
  "results": [
    {
      "score": 0.89,
      "text": "# ZKML\nJolt Atlas enables verifiable ML inference...",
      "tag": "zkml,research"
    }
  ],
  "monad_tx": "0xghi789...",
  "num_results": 1
}
```

### 4. Get Stats

View blockchain statistics:

```bash
curl http://localhost:8000/stats
```

Response:
```json
{
  "total_memories_on_chain": 42,
  "agent_memories": 12,
  "contract_address": "0x...",
  "agent_address": "0xDA9f4e4C9596a1dA338164FD22895D8C167C6Bd6"
}
```

## Troubleshooting

**"ic-py import error"**

Install dependencies:
```bash
pip install -r requirements.txt
# This installs ic-py>=2.0.0 from PyPI
```

**"Failed to connect to Monad"**
```bash
# Test mainnet RPC (use your RPC key)
curl https://rpc-mainnet.monadinfra.com/rpc/YOUR_KEY \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

**"IC identity not found"**

Make sure you have `IC_IDENTITY_PEM` in your `.env`:
```bash
IC_IDENTITY_PEM=-----BEGIN EC PRIVATE KEY-----
MHcCAQEEII...
-----END EC PRIVATE KEY-----
```

Get your identity PEM:
```bash
# If you have dfx installed
dfx identity export default > identity.pem
cat identity.pem  # Copy this to IC_IDENTITY_PEM
```

**"Anthropic API key invalid"**

Check your `.env` file has:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
```

**"Monad contract address not set"**

This is expected! Contract deployment is waiting for MON tokens. The app will work without Monad logging for now (IC storage and AI agent still functional).

## Next Steps

### Immediate:
- [x] IC Canister deployed and tested
- [x] AI Agent integrated (Claude Haiku)
- [x] All backend code complete
- [ ] Wait for Monad tokens from team
- [ ] Deploy Monad smart contract
- [ ] Deploy to Render
- [ ] Build frontend pages (foundation already exists)

### Future Enhancements:
- [ ] Add more content to build knowledge base
- [ ] Multi-user support with wallet authentication
- [ ] Conversation history persistence
- [ ] Analytics dashboard
- [ ] Custom LLM models or local deployment

## Current Architecture

```
User → FastAPI (Render) → Claude AI + Kinic (IC) + Monad
                           ✅ Working   ✅ Working   ⏳ Pending
```

## Need Help?

- 📚 **Full documentation**: `README.md`
- 🏗️ **Architecture details**: See README architecture diagram
- 📡 **API docs**: See README API endpoints section
- 🔧 **IC canister**: Already deployed at `2x5sz-ciaaa-aaaak-apgta-cai`
- 💰 **Monad tokens**: Contact Monad team for address `0xDA9f4e4C9596a1dA338164FD22895D8C167C6Bd6`

---

**Status**: ✅ 95% Complete | ⏳ Waiting for Monad Tokens | 🚀 Ready to Deploy

**Last Updated**: November 2025
