# Running Backend on Windows with Full Kinic Support

This guide shows you how to run the backend on Windows to enable full Kinic (Internet Computer) storage functionality.

## Why Windows?

- **WSL Issue**: WSL doesn't have a keyring service, so `kinic-cli` can't access IC credentials
- **Windows Solution**: `kinic-cli.exe` uses Windows Credential Manager for secure credential storage
- **Result**: Full Kinic functionality with memory storage on Internet Computer

## Prerequisites

1. ✅ `kinic-cli.exe` built and working (you mentioned you have this)
2. ✅ Python virtual environment with all dependencies installed
3. ✅ `.env` file with all credentials

## Quick Start

### Option 1: Using PowerShell Script (Easiest)

1. Open **PowerShell** in your project directory
2. Run the startup script:
```powershell
.\start_backend_windows.ps1
```

### Option 2: Manual Start

1. Open **PowerShell** in your project directory
2. Activate the virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
```

3. Start the backend:
```powershell
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Verification

You should see output like:
```
============================================================
🚀 Starting Kinic Memory Agent on Monad
============================================================

🔐 Loading credentials from OS keyring...
✅ Credentials loaded successfully

📦 Initializing Kinic Runner...
✅ KinicRunner initialized with CLI at: .\kinic-cli\target\release\kinic-cli.exe

🔗 Initializing Monad Logger...
✅ Connected to Monad! Chain ID: 143
📝 Using account: 0xDA9f4e4C9596a1dA338164FD22895D8C167C6Bd6
📜 Contract loaded at: 0xEB5B78Fa81cFEA1a46D46B3a42814F5A68038548

🤖 Initializing AI Agent (Claude Haiku)...

============================================================
✅ All services initialized successfully!
============================================================
```

**Key difference from WSL**: You should **NOT** see "Keychain Error" when inserting memories!

## Frontend Configuration

### If Frontend Running in WSL

Update `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://172.30.160.1:8000
```

Replace `172.30.160.1` with your Windows WSL IP (find with `ipconfig` in Windows, look for WSL adapter).

### If Frontend Running in Windows

Keep `frontend/.env.local` as:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Testing Full Kinic Functionality

1. Visit `http://localhost:3000/memories`
2. Click "Add Memory"
3. Enter content: "Testing Kinic IC storage from Windows!"
4. Add tags: "test,windows,kinic"
5. Click "Save Memory"

You should see:
- ✅ Memory saved to Kinic (Internet Computer)
- ✅ Metadata logged to Monad blockchain
- ✅ Transaction hash displayed
- ✅ No keyring errors!

## Troubleshooting

### "kinic-cli.exe not found"
Build it with:
```powershell
cd kinic-cli
cargo build --release
```

### "Port 8000 already in use"
Kill any running backends:
```powershell
Get-Process -Name python | Where-Object {$_.Path -like "*uvicorn*"} | Stop-Process -Force
```

### Credentials Not Found
Make sure your `.env` file has all required variables:
- `KINIC_MEMORY_ID`
- `IC_IDENTITY_NAME`
- `MONAD_RPC_URL`
- `MONAD_PRIVATE_KEY`
- `MONAD_CONTRACT_ADDRESS`
- `ANTHROPIC_API_KEY`

## Architecture

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────────┐
│  Frontend   │────────▶│  Python Backend  │────────▶│  kinic-cli.exe  │
│ (Port 3000) │         │   (Port 8000)    │         │                 │
│             │         │                  │         │  Uses Windows   │
│ WSL or Win  │         │   Windows Only   │         │  Credential Mgr │
└─────────────┘         └──────────────────┘         └─────────────────┘
                               │                              │
                               │                              ▼
                               │                     ┌─────────────────┐
                               │                     │ Internet        │
                               │                     │ Computer (IC)   │
                               │                     │ Kinic Canister  │
                               │                     └─────────────────┘
                               ▼
                        ┌─────────────────┐
                        │ Monad Blockchain│
                        │ (Metadata Only) │
                        └─────────────────┘
```

## Next Steps

Once backend is running on Windows:
1. Frontend can connect from WSL or Windows
2. All memory operations will use both Kinic (IC) and Monad
3. No more "keyring unavailable" warnings
4. Full semantic search capabilities enabled
