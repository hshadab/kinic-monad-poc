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

### ✅ **FULLY DEPLOYED & LIVE:**
- ✅ **Internet Computer Canister**: `2x5sz-ciaaa-aaaak-apgta-cai`
- ✅ **Monad Smart Contract**: Deployed on Monad Mainnet
- ✅ **Render Deployment**: https://monad-ai-memory.onrender.com
- ✅ **AI Agent**: Claude Haiku integrated
- ✅ **Frontend**: Next.js app with Chat, Memories, Dashboard pages
- ✅ **API Endpoints**: /insert, /search, /chat, /stats, /health
- ✅ **Metadata Extraction**: Automated title/summary/tags
- ✅ **Blockchain Logging**: All operations logged to Monad

### 🎯 **Production Ready**
All features working end-to-end. Ready for testing and demos!

---

## 📡 **API Endpoints**

### `POST /chat` - AI Conversation
Talk with the AI agent using memories as context.

```bash
curl -X POST https://monad-ai-memory.onrender.com/chat \
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
curl -X POST https://monad-ai-memory.onrender.com/insert \
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
curl -X POST https://monad-ai-memory.onrender.com/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "blockchain performance",
    "top_k": 5
  }'
```

### `GET /stats` - Blockchain Statistics
View on-chain memory statistics.

```bash
curl https://monad-ai-memory.onrender.com/stats
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
curl https://monad-ai-memory.onrender.com/health
```

**Response:**
```json
{
  "status": "healthy",
  "kinic": "connected",
  "monad": "connected",
  "memory_id": "2x5sz-ciaaa-aaaak-apgta-cai"
}
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

### **Frontend**
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Brutalist Kinic design system
- **Axios** - API client
- **Deployed on Render** - Same-domain static + API

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

### **Live Deployment**

The application is currently deployed and running at:
- **URL**: https://monad-ai-memory.onrender.com
- **Platform**: Render.com
- **Frontend**: Next.js static export served by FastAPI
- **Backend**: FastAPI with Uvicorn
- **Database**: Internet Computer Canister `2x5sz-ciaaa-aaaak-apgta-cai`
- **Blockchain**: Monad Mainnet (contract deployed)

### **Deploy Your Own Instance**

#### 1. Fork Repository
```bash
git clone https://github.com/your-username/kinic-monad-poc
cd kinic-monad-poc
```

#### 2. Set Up Credentials

Create environment variables on Render:

```bash
# Monad (get your own)
MONAD_RPC_URL=https://rpc-mainnet.monadinfra.com/rpc/YOUR_API_KEY
MONAD_CONTRACT_ADDRESS=0xYOUR_CONTRACT_ADDRESS
MONAD_PRIVATE_KEY=0xYOUR_PRIVATE_KEY

# Internet Computer (get IC identity)
KINIC_MEMORY_ID=your-canister-id
IC_IDENTITY_PEM=-----BEGIN EC PRIVATE KEY-----\nYOUR_IDENTITY\n-----END EC PRIVATE KEY-----

# AI (get from Anthropic)
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY
```

**Important**: Never commit `.env` files or credentials to git! They are gitignored for security.

#### 3. Deploy to Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect your repository
4. Set environment type: **Docker**
5. Add all environment variables above
6. Deploy!

Build time: ~8-12 minutes (Rust + Node + Python build)

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

### **Phase 1: MVP** ✅ COMPLETE
- ✅ IC canister deployed on Internet Computer
- ✅ AI agent integrated (Claude Haiku)
- ✅ API complete with all endpoints
- ✅ Monad contract deployed to mainnet
- ✅ Full deployment on Render.com
- ✅ Frontend with Chat, Memories, Dashboard pages
- ✅ Docker multi-stage build (Rust + Node + Python)

### **Phase 2: Enhancements** (Planned)
- 🔐 Wallet-based authentication (MetaMask/WalletConnect)
- 📁 Per-user memory isolation
- 💰 User-paid transactions
- 🎨 Enhanced UI/UX
- 📱 Mobile-responsive design improvements

### **Phase 3: Advanced Features** (Future)
- 🔍 Advanced semantic features (clustering, similarity graphs)
- 💬 Conversation history and threading
- 📈 Analytics dashboard with visualizations
- 🔗 Cross-agent knowledge sharing
- 🌐 Multi-chain support

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

---

## 🎉 **Try It Now!**

**Live Demo**: https://monad-ai-memory.onrender.com

- 💬 Chat with AI agent
- 📝 Store and search memories
- 📊 View blockchain stats
- ⛓️ All operations logged on Monad

---

**Status**: ✅ **FULLY DEPLOYED & OPERATIONAL**

**Last Updated**: November 17, 2025
