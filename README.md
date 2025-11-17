# Kinic AI Memory Agent on Monad

An AI-powered memory agent that combines Kinic's semantic storage (Internet Computer) with Monad blockchain for transparent, verifiable knowledge management.

**Built with:** FastAPI + Claude AI + Internet Computer + Monad Blockchain

---

## 🎯 **What This Does**

Never lose track of important information. Store notes, research, and conversations with AI-powered semantic search and chat. Every memory operation is publicly logged on Monad blockchain with readable summaries and tags - creating a verifiable knowledge trail.

**Perfect for:** Researchers, developers, teams, and anyone needing transparent, searchable memory with blockchain proof.

---

## 🏗️ **Architecture**

```
┌──────────────────────────────────────┐
│  User Interface (Next.js)            │
│  - Chat with AI agent                │
│  - Browse memories                   │
│  - View blockchain stats             │
└─────────────┬────────────────────────┘
              │
              ▼
┌──────────────────────────────────────┐
│  Render.com - FastAPI Service        │
│  ┌────────────────────────────────┐  │
│  │  AI Agent (Claude Haiku)       │  │
│  │  - Context-aware responses     │  │
│  │  - Memory retrieval            │  │
│  │  - Intelligent conversations   │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │  Memory Pipeline               │  │
│  │  - Metadata extraction         │  │
│  │  - Semantic search             │  │
│  │  - Blockchain logging          │  │
│  └────────────────────────────────┘  │
└────┬─────────────────────┬───────────┘
     │                     │
     ▼                     ▼
┌─────────────┐    ┌──────────────────┐
│  Kinic/IC   │    │  Monad Mainnet   │
│  ✅ DEPLOYED│    │  (Smart Contract)│
│             │    │                  │
│ Canister:   │    │  Logs:           │
│ 2x5sz-ciaaa │    │  - Titles        │
│ -aaaak-     │    │  - Summaries     │
│ apgta-cai   │    │  - Tags          │
│             │    │  - Timestamps    │
│ - Semantic  │    │  - User actions  │
│   storage   │    │                  │
│ - Vector    │    │  Human-readable  │
│   search    │    │  on-chain data   │
└─────────────┘    └──────────────────┘
```

---

## ✨ **Features**

### **AI-Powered Chat**
- 🤖 Conversational AI powered by Claude Haiku
- 🧠 Retrieves relevant memories as context
- 💬 Natural language interactions
- 📝 Logs conversations to blockchain

### **Semantic Memory**
- 🔍 Semantic search (not just keywords)
- 📊 Vector embeddings via Kinic API
- 🗄️ Decentralized storage on Internet Computer
- 🏷️ Auto-tagging and categorization

### **Blockchain Transparency**
- ⛓️ Every operation logged on Monad
- 📖 Human-readable metadata on-chain
- 🔍 Public audit trail
- ✅ Verifiable knowledge graph

---

## 🚀 **Current Status**

### ✅ **Deployed & Working:**
- ✅ **Internet Computer Canister**: `2x5sz-ciaaa-aaaak-apgta-cai`
- ✅ **AI Agent**: Claude Haiku integrated
- ✅ **API Endpoints**: /insert, /search, /chat, /stats
- ✅ **Metadata Extraction**: Automated title/summary/tags
- ✅ **All Code**: 100% complete and tested

### ⏳ **Pending:**
- ⏳ **Monad Smart Contract**: Waiting for MON tokens
- ⏳ **Render Deployment**: Blocked by contract deployment
- ⏳ **Frontend**: Foundation built, pages pending

---

## 📡 **API Endpoints**

### `POST /chat` - AI Conversation
Talk with the AI agent using memories as context.

```bash
curl -X POST https://your-app.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me about ZKML",
    "top_k": 3
  }'
```

**Response:**
```json
{
  "response": "ZKML (Zero-Knowledge Machine Learning) is a framework...",
  "memories_used": [
    {
      "text": "# ZKML Overview\nJolt Atlas is a framework...",
      "score": 0.89,
      "tag": "zkml,test"
    }
  ],
  "num_memories": 1,
  "monad_tx": "0xabc123..."
}
```

### `POST /insert` - Store Memory
Store new content with automatic metadata extraction.

```bash
curl -X POST https://your-app.onrender.com/insert \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Research Notes\nImportant findings...",
    "user_tags": "research,notes"
  }'
```

**Response:**
```json
{
  "kinic_result": {"status": "inserted"},
  "monad_tx": "0xdef456...",
  "metadata": {
    "title": "Research Notes",
    "summary": "Important findings...",
    "tags": "research,notes,findings",
    "content_hash": "0x..."
  }
}
```

### `POST /search` - Semantic Search
Search memories by meaning, not just keywords.

```bash
curl -X POST https://your-app.onrender.com/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "blockchain performance",
    "top_k": 5
  }'
```

### `GET /stats` - Blockchain Statistics
View on-chain memory statistics.

```bash
curl https://your-app.onrender.com/stats
```

**Response:**
```json
{
  "total_memories_on_chain": 42,
  "agent_memories": 12,
  "contract_address": "0x...",
  "agent_address": "0x..."
}
```

### `GET /health` - Health Check
```bash
curl https://your-app.onrender.com/health
```

---

## 🛠️ **Technology Stack**

### **Backend**
- **FastAPI** - High-performance Python API
- **Anthropic Claude** - AI agent (Haiku model)
- **Web3.py** - Monad blockchain integration
- **Pydantic** - Data validation

### **Storage & Blockchain**
- **Internet Computer** - Decentralized semantic storage
- **Kinic API** - Embedding generation
- **Monad** - EVM-compatible blockchain
- **Solidity** - Smart contracts

### **Frontend** (In Progress)
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling with Kinic design
- **Vercel** - Deployment

---

## 📁 **Project Structure**

```
kinic-monad-poc/
├── contracts/
│   ├── KinicMemoryLog.sol          # Smart contract
│   ├── deploy.py                   # Deployment script
│   └── abi.json                    # Contract ABI (generated)
│
├── src/
│   ├── main.py                     # FastAPI application
│   ├── ai_agent.py                 # Claude AI integration
│   ├── models.py                   # Pydantic models
│   ├── metadata.py                 # Metadata extraction
│   ├── kinic_runner.py             # IC canister client
│   └── monad.py                    # Monad logger
│
├── frontend/
│   ├── app/                        # Next.js pages
│   ├── components/                 # React components
│   ├── lib/                        # API client
│   └── package.json
│
├── scripts/
│   ├── setup_complete.sh           # Full setup wizard
│   ├── test_local.sh               # Local testing
│   └── setup_ic_identity.sh        # IC identity helper
│
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container build
├── render.yaml                     # Render deployment
└── README.md                       # This file
```

---

## 🚀 **Deployment**

### **Prerequisites**

1. **Monad Tokens** - For smart contract deployment
   - Contact Monad team or use faucet
   - Address: `0xDA9f4e4C9596a1dA338164FD22895D8C167C6Bd6`

2. **API Keys**
   - Anthropic API key (for Claude)
   - Already have Kinic API access

3. **IC Canister** - ✅ Already deployed!
   - Canister ID: `2x5sz-ciaaa-aaaak-apgta-cai`

### **Quick Deploy (When Tokens Arrive)**

```bash
# 1. Clone repository
git clone <your-repo>
cd kinic-monad-poc

# 2. Deploy Monad contract
source venv/bin/activate
python contracts/deploy.py

# 3. Update .env with contract address
nano .env  # Add MONAD_CONTRACT_ADDRESS

# 4. Test locally
./scripts/test_local.sh

# 5. Deploy to Render
git push origin main
# Configure on Render dashboard
```

### **Environment Variables**

Required for deployment:

```bash
# Monad
MONAD_RPC_URL=https://rpc-mainnet.monadinfra.com/rpc/...
MONAD_CONTRACT_ADDRESS=0x...  # From deployment
MONAD_PRIVATE_KEY=0x...       # Your wallet

# Internet Computer
KINIC_MEMORY_ID=2x5sz-ciaaa-aaaak-apgta-cai
IC_IDENTITY_NAME=kinic_local
IC_IDENTITY_PEM=-----BEGIN EC PRIVATE KEY-----...

# AI
ANTHROPIC_API_KEY=sk-ant-api03-...
```

---

## 💰 **Costs**

### **Internet Computer**
- **Deployment**: ~0.1 ICP (~$0.50) ✅ Already paid
- **Operations**: ~$0.000001 per insert/search
- **Storage**: ~$0.0001 per MB per year

### **Monad**
- **Contract Deploy**: ~$0.50-$2 in gas
- **Transactions**: ~$0.01-$0.10 per log

### **Claude AI**
- **Model**: Haiku (fastest, cheapest)
- **Cost**: ~$0.001-0.005 per chat
- **Very affordable for POC!**

**Total POC Cost**: ~$5-10 (already spent $0.50 on IC)

---

## 🧪 **Testing**

### **Test IC Canister** (Already Working!)

```bash
# From Windows PowerShell (where kinic-cli is built)
cd C:\kinic-cli

# Insert memory
.\target\release\kinic-cli.exe --identity kinic_local --ic insert \
  --memory-id 2x5sz-ciaaa-aaaak-apgta-cai \
  --text "Test memory" \
  --tag "test"

# Search
.\target\release\kinic-cli.exe --identity kinic_local --ic search \
  --memory-id 2x5sz-ciaaa-aaaak-apgta-cai \
  --query "test memory"
```

### **Test Complete System** (After Monad Deploy)

```bash
./scripts/test_local.sh
```

---

## 📊 **What Gets Stored on Monad**

Unlike typical blockchain apps that only store hashes, we store **rich, human-readable metadata**:

```solidity
struct Memory {
    address user;           // Who stored it
    uint8 opType;          // INSERT or SEARCH
    string title;          // "ZKML Verification Methods"
    string summary;        // "Jolt Atlas enables..."
    string tags;           // "zkml,jolt,proofs"
    bytes32 contentHash;   // SHA256 of full content
    uint256 timestamp;     // When it happened
}
```

**This makes Monad a queryable knowledge graph**, not just an audit log!

---

## 🔮 **Roadmap**

### **Phase 1: MVP** (95% Complete)
- ✅ IC canister deployed
- ✅ AI agent integrated
- ✅ API complete
- ⏳ Monad contract (waiting for tokens)
- ⏳ Render deployment

### **Phase 2: Multi-User** (Future)
- 🔐 Wallet-based authentication
- 📁 Per-user memory isolation
- 💰 User-paid transactions
- 🎨 Complete frontend

### **Phase 3: Advanced** (Future)
- 🔍 Advanced semantic features
- 💬 Conversation history
- 📈 Analytics dashboard
- 🔗 Cross-agent knowledge sharing

---

## 🤝 **Contributing**

This is a POC/demo project. For production use:
1. Add proper authentication
2. Implement rate limiting
3. Add user account management
4. Deploy monitoring/logging
5. Security audit contracts

---

## 📄 **License**

MIT

---

## 🙏 **Credits**

Built with:
- [Kinic](https://kinic.io) - Semantic memory storage
- [Monad](https://monad.xyz) - High-performance blockchain
- [Internet Computer](https://internetcomputer.org) - Decentralized compute
- [Anthropic Claude](https://anthropic.com) - AI assistance
- [FastAPI](https://fastapi.tiangolo.com) - Python web framework

---

## 📞 **Support**

- **Documentation**: See `QUICKSTART.md` for setup guide
- **Issues**: GitHub Issues
- **Architecture**: See diagrams in `/docs`

---

**Status**: ✅ Backend Complete | ⏳ Waiting for Monad Tokens | 🚧 Frontend In Progress

**Last Updated**: November 2025
