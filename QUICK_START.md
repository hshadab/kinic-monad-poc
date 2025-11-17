# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Check Prerequisites

```bash
# Verify Python version (3.8+)
python --version

# Verify you're in the correct directory
pwd
# Should show: C:/Users/hshad/kinic-backend-windows (or similar)

# Check if kinic-cli exists (Rust binary)
ls kinic-cli/target/release/kinic-cli  # or wherever it's located
```

### Step 2: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

### Step 3: Setup Credentials (Secure Method)

```bash
# Run interactive credential setup
python setup_credentials.py
```

**You'll be prompted for:**
1. Monad Private Key (Ethereum private key with 0x prefix)
2. Anthropic API Key (from https://console.anthropic.com/)
3. Kinic Memory ID (IC canister principal)
4. IC Identity Name (press Enter for "default")
5. Monad RPC URL (press Enter for testnet default)

**Then set the contract address:**
```bash
# Windows CMD
set MONAD_CONTRACT_ADDRESS=0xYourContractAddress

# Windows PowerShell
$env:MONAD_CONTRACT_ADDRESS="0xYourContractAddress"

# Linux/Mac
export MONAD_CONTRACT_ADDRESS=0xYourContractAddress
```

### Step 4: Run the Application

```bash
python -m src.main
```

**Expected output:**
```
============================================================
🚀 Starting Kinic Memory Agent on Monad
============================================================

🔐 Loading credentials from OS keyring...
✅ Credentials loaded successfully

📦 Initializing Kinic Runner...
✅ KinicRunner initialized with CLI at: ./kinic-cli

🔗 Initializing Monad Logger...
✅ Connected to Monad! Chain ID: 10143
📝 Using account: 0xYour...Address
📜 Contract loaded at: 0xYour...Contract

🤖 Initializing AI Agent (Claude Haiku)...

============================================================
✅ All services initialized successfully!
============================================================

INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Test the API

**Open a new terminal and try:**

```bash
# Test health check
curl http://localhost:8000/health

# Test insert
curl -X POST http://localhost:8000/insert \
  -H "Content-Type: application/json" \
  -d '{"content": "# Test\nThis is my first memory!", "user_tags": "test"}'

# Test search
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "first memory", "top_k": 5}'
```

**Or visit the interactive docs:**
- http://localhost:8000/docs

---

## 🔧 Alternative Setup (Environment Variables)

If you prefer environment variables over keyring:

```bash
# Windows CMD
set MONAD_PRIVATE_KEY=0xYourPrivateKey
set ANTHROPIC_API_KEY=sk-ant-your-key
set KINIC_MEMORY_ID=your-canister-id
set IC_IDENTITY_NAME=default
set MONAD_RPC_URL=https://testnet-rpc.monad.xyz
set MONAD_CONTRACT_ADDRESS=0xYourContractAddress

# Windows PowerShell
$env:MONAD_PRIVATE_KEY="0xYourPrivateKey"
$env:ANTHROPIC_API_KEY="sk-ant-your-key"
$env:KINIC_MEMORY_ID="your-canister-id"
$env:IC_IDENTITY_NAME="default"
$env:MONAD_RPC_URL="https://testnet-rpc.monad.xyz"
$env:MONAD_CONTRACT_ADDRESS="0xYourContractAddress"

# Linux/Mac
export MONAD_PRIVATE_KEY=0xYourPrivateKey
export ANTHROPIC_API_KEY=sk-ant-your-key
export KINIC_MEMORY_ID=your-canister-id
export IC_IDENTITY_NAME=default
export MONAD_RPC_URL=https://testnet-rpc.monad.xyz
export MONAD_CONTRACT_ADDRESS=0xYourContractAddress
```

Then run: `python -m src.main`

---

## 📋 Common Issues

### Issue 1: "kinic-cli binary not found"
**Fix**:
```bash
# Build the Rust CLI first
cd kinic-cli
cargo build --release
cd ..
```

### Issue 2: "Credentials not found"
**Fix**:
```bash
# View what's stored
python setup_credentials.py view

# Re-run setup
python setup_credentials.py
```

### Issue 3: "Failed to connect to Monad"
**Fix**: Check your RPC URL is correct and accessible
```bash
curl https://testnet-rpc.monad.xyz
```

### Issue 4: "ABI file not found"
**Fix**: Create contracts directory and add ABI
```bash
mkdir contracts
# Copy your KinicMemoryLog ABI JSON to contracts/abi.json
```

---

## 📚 What's Next?

1. **Read the full README**: [README.md](README.md)
2. **Understand the architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
3. **Learn about credentials**: [CREDENTIAL_SETUP.md](CREDENTIAL_SETUP.md)
4. **Try the chat endpoint**: See README for examples

---

## 🎯 Quick Command Reference

```bash
# Start server
python -m src.main

# Setup credentials
python setup_credentials.py

# View credentials
python setup_credentials.py view

# Delete credentials
python setup_credentials.py delete

# Test health
curl http://localhost:8000/health

# Interactive API docs
# Open browser: http://localhost:8000/docs
```

---

**You're all set! 🎉**

For detailed documentation, see [README.md](README.md)
