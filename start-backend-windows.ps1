# PowerShell script to run the backend from Windows
# This ensures kinic-cli can access Windows Credential Manager for IC identity

Write-Host "Starting Kinic Monad POC Backend from Windows..." -ForegroundColor Green

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Check if virtual environment exists
if (-Not (Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "Error: Virtual environment not found at .\venv\Scripts\Activate.ps1" -ForegroundColor Red
    Write-Host "Please create a virtual environment first:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor Yellow
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Check if uvicorn is installed
try {
    $null = Get-Command python -ErrorAction Stop
    Write-Host "Python found: $(python --version)" -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found in virtual environment" -ForegroundColor Red
    exit 1
}

# Start the backend
Write-Host "Starting backend on http://0.0.0.0:8000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
