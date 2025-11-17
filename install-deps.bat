@echo off
cd /d "%~dp0"
echo Installing dependencies in Windows venv...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install fastapi uvicorn[standard] pydantic web3 eth-account py-solc-x httpx anthropic python-dotenv keyring
echo.
echo Installation complete!
pause
