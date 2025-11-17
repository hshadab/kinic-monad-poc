# Kinic Memory Agent - Windows Backend Startup Script
# This script starts the FastAPI backend with full Kinic (IC) functionality

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 Starting Kinic Memory Agent Backend (Windows)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create it first with: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Check if .env exists
if (-Not (Test-Path ".\.env")) {
    Write-Host "WARNING: .env file not found!" -ForegroundColor Yellow
    Write-Host "Make sure environment variables are set in Windows." -ForegroundColor Yellow
}

# Check if kinic-cli.exe exists
if (Test-Path ".\kinic-cli\target\release\kinic-cli.exe") {
    Write-Host "✅ Found kinic-cli.exe - Kinic storage will work!" -ForegroundColor Green
} else {
    Write-Host "WARNING: kinic-cli.exe not found at .\kinic-cli\target\release\kinic-cli.exe" -ForegroundColor Yellow
    Write-Host "Build it with: cd kinic-cli; cargo build --release" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🌐 Starting backend server on http://0.0.0.0:8000..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Start uvicorn
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
