# Architecture Documentation

## System Overview

Kinic Backend is a **hybrid decentralized application** that combines three major technologies to create an AI-powered memory system with blockchain transparency.

### Core Technologies

| Technology | Role | Purpose |
|------------|------|---------|
| **Internet Computer (IC)** | Storage Layer | Scalable, decentralized memory storage via canisters |
| **Monad Blockchain** | Metadata Layer | Transparent, immutable logging of operations |
| **Claude AI (Anthropic)** | Intelligence Layer | Context-aware conversational AI |

---

## Detailed Architecture

### Layer 1: API Layer (FastAPI)

**File**: `src/main.py`

**Responsibilities**:
- HTTP endpoint handling
- Request validation (via Pydantic)
- Service orchestration
- CORS middleware
- Lifespan management (startup/shutdown)

**Endpoints**:
```python
GET  /              # Service info
GET  /health        # Health check
POST /insert        # Store memory
POST /search        # Search memories
POST /chat          # Chat with AI
GET  /stats         # Blockchain stats
```

**Lifecycle**:
```
Startup (lifespan):
  1. Load credentials from OS keyring
  2. Initialize KinicRunner (IC connection)
  3. Initialize MonadLogger (blockchain connection)
  4. Initialize AIAgent (Claude connection)

Runtime:
  - Handle incoming requests
  - Coordinate between services
  - Return structured responses

Shutdown:
  - Cleanup resources
  - Close connections
```

### Layer 2: Service Layer

#### A. Kinic Runner (`kinic_runner.py`)

**Purpose**: Bridge between Python backend and Rust kinic-cli binary

**Architecture**:
```
Python (FastAPI) → subprocess → kinic-cli (Rust) → IC Canister
```

**Key Operations**:

1. **INSERT**:
```python
Content → temp file → kinic-cli insert → IC canister → Result
```

2. **SEARCH**:
```python
Query → kinic-cli search → IC canister → Parse JSON → Results
```

**Communication Protocol**:
- Input: Command-line arguments + temp files
- Output: stdout (JSON or text)
- Error: stderr (error messages)

**CLI Command Structure**:
```bash
kinic-cli --identity <name> <command> --memory-id <id> [args]

Examples:
kinic-cli --identity default insert --memory-id abc123 --file-path /tmp/content.txt --tag "research"
kinic-cli --identity default search --memory-id abc123 --query "zkml verification"
```

#### B. Monad Logger (`monad.py`)

**Purpose**: Interface to KinicMemoryLog smart contract on Monad EVM

**Architecture**:
```
Python → Web3.py → RPC Provider → Monad Node → Smart Contract
```

**Smart Contract Interface**:

```solidity
// Contract: KinicMemoryLog
contract KinicMemoryLog {
    struct MemoryLog {
        address user;
        uint8 opType;      // 0=INSERT, 1=SEARCH
        string title;
        string summary;
        string tags;
        bytes32 contentHash;
        uint256 timestamp;
    }

    event MemoryLogged(
        address indexed user,
        uint8 opType,
        string title,
        string summary,
        string tags,
        bytes32 contentHash,
        uint256 timestamp
    );

    function logMemory(...) external returns (bytes32)
    function getUserMemories(address user) external view returns (MemoryLog[])
    function getTotalMemories() external view returns (uint256)
}
```

**Transaction Flow**:
```
1. Build transaction (logMemory call)
2. Sign with private key (eth_account)
3. Send to Monad RPC
4. Wait for confirmation
5. Return transaction hash
```

**Gas Management**:
- Automatically estimates gas
- Uses account's ETH balance for fees
- No explicit gas price setting (relies on RPC)

#### C. AI Agent (`ai_agent.py`)

**Purpose**: Claude AI integration with memory-aware context

**Architecture**:
```
User Query → Search Memories → Build Context → Claude API → Response
```

**Context Building**:
```python
# Input: Search results from Kinic
results = [
    {"text": "...", "score": 0.89, "tag": "zkml"},
    {"text": "...", "score": 0.75, "tag": "research"},
    ...
]

# Output: Formatted context for Claude
context = """
[Memory 1] (relevance: 0.89, tags: zkml)
Zero-knowledge machine learning enables...

[Memory 2] (relevance: 0.75, tags: research)
Recent advances in zkML verification...
"""
```

**Prompt Structure**:
```
System Prompt:
  → Define agent's role and capabilities

Context (if available):
  → Top N relevant memories

User Message:
  → Current question/request

Previous Conversation (optional):
  → Chat history for continuity
```

**Response Generation**:
- Model: Claude 3 Haiku (fast, cost-effective)
- Max tokens: 1024
- Temperature: Default
- System prompt: Memory agent persona

#### D. Metadata Extractor (`metadata.py`)

**Purpose**: Extract structured metadata without LLM (cost-free, fast)

**Extraction Pipeline**:

```
Input Content
    ↓
┌───────────────────┐
│ Title Extraction  │ → Check for # headings → First line fallback
└───────────────────┘
    ↓
┌───────────────────┐
│Summary Extraction │ → Remove markdown → First paragraph → Truncate
└───────────────────┘
    ↓
┌───────────────────┐
│ Tag Extraction    │ → Lowercase → Extract words → Remove stopwords
└───────────────────┘   → Count frequency → Top 5 words
    ↓
┌───────────────────┐
│  Hash Generation  │ → SHA256(content) → Add 0x prefix
└───────────────────┘
    ↓
Metadata Object
```

**Algorithms**:

1. **Title**: Regex for markdown headers (`#+ Title`)
2. **Summary**: Paragraph split, length filter, truncate
3. **Tags**: Word frequency (Counter), stopword filter
4. **Hash**: SHA256 in hex with 0x prefix (blockchain compatible)

#### E. Credential Manager (`credential_manager.py`)

**Purpose**: Secure credential storage using OS-native keyring

**Architecture by Platform**:

```
┌─────────────────────────────────────────────────────┐
│              CredentialManager                      │
│                 (Python)                             │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
    Windows     macOS      Linux
        │          │          │
┌───────▼──────┐ ┌▼────────┐ ┌▼──────────────┐
│  Credential  │ │ Keychain │ │ Secret Service│
│   Manager    │ │  Access  │ │ API (D-Bus)   │
└──────────────┘ └──────────┘ └───────────────┘
```

**Storage Format**:
```
Service Name: "kinic-backend"
Credential Keys:
  - monad_private_key
  - anthropic_api_key
  - ic_identity_name
  - kinic_memory_id
  - monad_rpc_url
```

**Fallback Mechanism**:
```python
def get_credential(key, fallback_env_var):
    # Try keyring first
    value = keyring.get_password(service, key)
    if value:
        return value

    # Fall back to environment variable
    if fallback_env_var:
        return os.getenv(fallback_env_var)

    return None
```

---

## Data Flow Diagrams

### INSERT Operation (Detailed)

```
┌────────┐
│ Client │
└───┬────┘
    │ POST /insert
    │ {"content": "...", "user_tags": "..."}
    ↓
┌───────────────┐
│   FastAPI     │
│   Endpoint    │
└───┬───────────┘
    │ 1. Validate request (Pydantic)
    ↓
┌───────────────┐
│ KinicRunner   │
│   .insert()   │
└───┬───────────┘
    │ 2. Create temp file with content
    │ 3. Execute: kinic-cli insert --file-path /tmp/xxx
    │ 4. Await subprocess completion
    ↓
┌───────────────┐
│  kinic-cli    │
│  (Rust CLI)   │
└───┬───────────┘
    │ 5. Read file content
    │ 6. Connect to IC canister
    │ 7. Call canister's store method
    ↓
┌───────────────┐
│ IC Canister   │
│  (Storage)    │
└───┬───────────┘
    │ 8. Store in stable memory
    │ 9. Return success
    ↓
┌───────────────┐
│ KinicRunner   │
└───┬───────────┘
    │ 10. Parse CLI output
    │ 11. Return to FastAPI
    ↓
┌───────────────┐
│   FastAPI     │
└───┬───────────┘
    │ 12. Extract metadata (title, summary, tags, hash)
    ↓
┌───────────────┐
│ MonadLogger   │
│.log_insert()  │
└───┬───────────┘
    │ 13. Build transaction data
    │ 14. Sign with private key
    │ 15. Send to Monad RPC
    ↓
┌───────────────┐
│ Monad Node    │
│(Blockchain)   │
└───┬───────────┘
    │ 16. Execute contract call
    │ 17. Emit MemoryLogged event
    │ 18. Return tx hash
    ↓
┌───────────────┐
│   FastAPI     │
└───┬───────────┘
    │ 19. Build response
    ↓
┌────────┐
│ Client │
└────────┘
    Response: {
        "kinic_result": {...},
        "monad_tx": "0x...",
        "metadata": {...}
    }
```

### SEARCH Operation (Detailed)

```
┌────────┐
│ Client │
└───┬────┘
    │ POST /search
    │ {"query": "...", "top_k": 5}
    ↓
┌───────────────┐
│   FastAPI     │
└───┬───────────┘
    │ 1. Validate request
    ↓
┌───────────────┐
│ KinicRunner   │
│  .search()    │
└───┬───────────┘
    │ 2. Execute: kinic-cli search --query "..."
    ↓
┌───────────────┐
│  kinic-cli    │
└───┬───────────┘
    │ 3. Connect to IC canister
    │ 4. Call canister's search method (semantic search)
    ↓
┌───────────────┐
│ IC Canister   │
└───┬───────────┘
    │ 5. Vector similarity search
    │ 6. Return ranked results
    ↓
┌───────────────┐
│ KinicRunner   │
└───┬───────────┘
    │ 7. Parse JSON results
    │ 8. Return to FastAPI
    ↓
┌───────────────┐
│   FastAPI     │
└───┬───────────┘
    │ 9. Extract query metadata
    ↓
┌───────────────┐
│ MonadLogger   │
│.log_search()  │
└───┬───────────┘
    │ 10. Log search operation to blockchain
    ↓
┌───────────────┐
│ Monad Node    │
└───┬───────────┘
    │ 11. Emit event, return tx hash
    ↓
┌───────────────┐
│   FastAPI     │
└───┬───────────┘
    │ 12. Format results
    ↓
┌────────┐
│ Client │
└────────┘
    Response: {
        "results": [...],
        "monad_tx": "0x...",
        "num_results": 5
    }
```

### CHAT Operation (Detailed)

```
┌────────┐
│ Client │
└───┬────┘
    │ POST /chat
    │ {"message": "...", "top_k": 3}
    ↓
┌───────────────┐
│   FastAPI     │
└───┬───────────┘
    │ 1. Validate request
    ↓
┌───────────────┐
│ KinicRunner   │
│  .search()    │
└───┬───────────┘
    │ 2. Search for relevant memories
    │    (same flow as SEARCH operation)
    ↓
┌───────────────┐
│   FastAPI     │
└───┬───────────┘
    │ 3. Format memories for AI
    ↓
┌───────────────┐
│   AIAgent     │
│    .chat()    │
└───┬───────────┘
    │ 4. Build context from memories
    │ 5. Construct prompt
    │ 6. Call Claude API
    ↓
┌───────────────┐
│ Anthropic API │
│  (Claude)     │
└───┬───────────┘
    │ 7. Process with context
    │ 8. Generate response
    ↓
┌───────────────┐
│   AIAgent     │
└───┬───────────┘
    │ 9. Return response text
    ↓
┌───────────────┐
│   FastAPI     │
└───┬───────────┘
    │ 10. Extract conversation metadata
    ↓
┌───────────────┐
│ MonadLogger   │
│.log_insert()  │
└───┬───────────┘
    │ 11. Log conversation to blockchain
    ↓
┌───────────────┐
│ Monad Node    │
└───┬───────────┘
    │ 12. Store on-chain
    ↓
┌───────────────┐
│   FastAPI     │
└───┬───────────┘
    │ 13. Build response
    ↓
┌────────┐
│ Client │
└────────┘
    Response: {
        "response": "...",
        "memories_used": [...],
        "monad_tx": "0x..."
    }
```

---

## Database Schema (IC Canister)

**Note**: Actual schema depends on kinic-cli implementation, but conceptually:

```
Memory Entry {
    id: Principal,
    content: Text,
    embedding: Vec<f32>,  // Vector for semantic search
    tag: Text,
    timestamp: Timestamp,
    user: Principal
}

Index:
    - Vector similarity index for embeddings
    - Tag-based index for filtering
    - Timestamp index for chronological access
```

---

## Blockchain Schema (Monad Smart Contract)

**Storage**:
```solidity
mapping(address => MemoryLog[]) public userMemories;
uint256 public totalMemories;

struct MemoryLog {
    address user;
    uint8 opType;        // 0=INSERT, 1=SEARCH
    string title;        // Max 100 chars
    string summary;      // Max 200 chars
    string tags;         // Comma-separated
    bytes32 contentHash; // SHA256
    uint256 timestamp;   // Block timestamp
}
```

**Events** (for indexing):
```solidity
event MemoryLogged(
    address indexed user,
    uint8 opType,
    string title,
    string summary,
    string tags,
    bytes32 contentHash,
    uint256 timestamp
);
```

---

## Security Architecture

### Credential Flow

```
Setup Phase:
  User → setup_credentials.py → OS Keyring
                                   ↓
                          Store encrypted credentials

Runtime Phase:
  FastAPI startup → CredentialManager → OS Keyring
                                          ↓
                                   Retrieve credentials
                                          ↓
                            Initialize services (Kinic, Monad, AI)

Fallback:
  Keyring unavailable → Environment Variables → Use if available
```

### Private Key Handling

```
1. Storage:   OS Keyring (encrypted) or ENV var
2. Loading:   CredentialManager.get_credential()
3. Usage:     MonadLogger.__init__()
4. Signing:   eth_account.Account.from_key()
5. Memory:    Stored in MonadLogger.account (protected attribute)
6. Logging:   NEVER logged (only account.address is logged)
```

### Request Authentication

**Current**: None (open API)

**Recommended for Production**:
```
1. API Key authentication
2. JWT tokens
3. Rate limiting
4. CORS restrictions
5. Request signing
```

---

## Performance Considerations

### Bottlenecks

1. **IC Canister Calls**: Network latency (200-500ms)
2. **Blockchain Transactions**: Block confirmation (2-5 seconds)
3. **Claude API**: Response generation (500-2000ms)

### Optimization Strategies

**Async Operations**:
```python
# All I/O is async
await kinic.insert(...)      # Non-blocking
await monad.log_insert(...)  # Non-blocking
await ai_agent.chat(...)     # Non-blocking
```

**Parallel Execution** (where applicable):
```python
# Could parallelize metadata logging while waiting for other ops
# (Currently sequential for simplicity)
```

**Caching** (not implemented, but possible):
- Cache frequent searches in Redis
- Cache AI responses for identical queries
- Cache blockchain state reads

---

## Error Handling

### Error Propagation

```
Layer 1 (FastAPI):
    Try/Catch → HTTPException → JSON error response

Layer 2 (Services):
    Try/Catch → Raise Exception → Propagate to Layer 1

Layer 3 (External):
    subprocess.returncode → Exception
    Web3 error → Exception
    API error → Exception
```

### Error Types

| Service | Error | Handling |
|---------|-------|----------|
| KinicRunner | CLI not found | FileNotFoundError → 503 |
| KinicRunner | CLI execution failed | Exception → 500 |
| MonadLogger | Connection failed | Exception → 503 |
| MonadLogger | Transaction reverted | Exception → 500 |
| AIAgent | API key invalid | AuthenticationError → 503 |
| AIAgent | Rate limit | RateLimitError → 429 |

---

## Scalability

### Current Limitations

- Single-instance FastAPI (no load balancing)
- Synchronous subprocess calls (one at a time)
- No request queuing
- No caching layer

### Scaling Strategies

**Horizontal Scaling**:
```
Load Balancer
    ↓
┌───────┬───────┬───────┐
│ API 1 │ API 2 │ API 3 │
└───────┴───────┴───────┘
    ↓       ↓       ↓
Shared Services (IC, Monad, Claude)
```

**Vertical Scaling**:
- Increase uvicorn workers
- Use process pooling for subprocess calls
- Optimize memory usage

**Caching**:
- Redis for search results
- Local cache for blockchain reads
- CDN for static responses

---

## Deployment Architecture

### Development
```
Local Machine
    ↓
Python venv → FastAPI → localhost:8000
```

### Production (Recommended)
```
┌─────────────────────────────────────┐
│          Load Balancer              │
└────────────┬────────────────────────┘
             │
    ┌────────┼────────┐
    ↓        ↓        ↓
┌────────┐ ┌────────┐ ┌────────┐
│ API 1  │ │ API 2  │ │ API 3  │
└────────┘ └────────┘ └────────┘
    │
    ↓
┌─────────────────────────────────────┐
│      External Services              │
├─────────────────────────────────────┤
│ - IC Network (decentralized)        │
│ - Monad RPC (can be self-hosted)    │
│ - Anthropic API (cloud)             │
└─────────────────────────────────────┘
```

---

## Monitoring & Observability

### Logging Points

1. **Startup**: Credential loading, service initialization
2. **Requests**: All endpoint calls with parameters
3. **IC Operations**: CLI commands, results, errors
4. **Blockchain**: Transaction hashes, gas usage, confirmations
5. **AI**: Model used, context size, response length

### Metrics to Track

- Request latency (per endpoint)
- IC call duration
- Blockchain transaction time
- AI response time
- Error rates by service
- Memory usage
- Active connections

### Health Checks

```
GET /health →
    ✓ Kinic: CLI accessible, canister reachable
    ✓ Monad: RPC connected, contract accessible
    ✓ (AI agent doesn't have health check currently)
```

---

**Last Updated**: 2025-11-16
**Version**: 1.0.0
