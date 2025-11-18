# Credential Setup Guide

## Overview

The Kinic Backend now uses **OS-level keyring** for secure credential storage instead of environment variables. This provides:

- ✅ **Better Security**: Credentials encrypted by your operating system
- ✅ **Convenience**: No need to set environment variables every time
- ✅ **Cross-Platform**: Works on Windows, macOS, and Linux

## Supported Platforms

| Platform | Storage Backend |
|----------|----------------|
| Windows  | Windows Credential Manager |
| macOS    | Keychain |
| Linux    | Secret Service API (freedesktop.org) |

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs the `keyring` library (version 25.6.0).

### 2. Run Credential Setup

```bash
python setup_credentials.py
```

The interactive script will guide you through storing:
- **Monad Private Key**: Your Ethereum private key for blockchain transactions
- **Anthropic API Key**: Claude AI API key
- **Kinic Memory ID**: Internet Computer canister memory ID
- **IC Identity Name**: DFX identity name (optional, default: "default")
- **Monad RPC URL**: Blockchain RPC endpoint (optional, default: testnet)

### 3. Set Contract Address (Environment Variable)

The contract address still uses an environment variable:

```bash
# Windows (Command Prompt)
set MONAD_CONTRACT_ADDRESS=0xYourContractAddress

# Windows (PowerShell)
$env:MONAD_CONTRACT_ADDRESS="0xYourContractAddress"

# Linux/macOS
export MONAD_CONTRACT_ADDRESS=0xYourContractAddress
```

### 4. Run the Application

```bash
python -m src.main
```

The application will automatically load credentials from the keyring!

## Command Reference

### Setup Credentials (Interactive)
```bash
python setup_credentials.py
```

### View Stored Credentials
```bash
python setup_credentials.py view
```

Shows which credentials are stored (with masking for sensitive values).

### Delete All Credentials
```bash
python setup_credentials.py delete
```

Removes all Kinic credentials from the OS keyring.

### Show Help
```bash
python setup_credentials.py help
```

## Migration from Environment Variables

The application supports **automatic fallback** to environment variables if credentials aren't found in the keyring. This allows gradual migration:

1. **Before Migration**: Uses environment variables
2. **During Migration**: Run `python setup_credentials.py`
3. **After Migration**: Credentials loaded from keyring, environment variables no longer needed

### Fallback Behavior

For each credential, the application:
1. First checks the OS keyring
2. If not found, falls back to environment variable
3. Logs a warning suggesting migration to keyring

Environment variable names:
- `MONAD_PRIVATE_KEY`
- `ANTHROPIC_API_KEY`
- `KINIC_MEMORY_ID`
- `IC_IDENTITY_NAME`
- `MONAD_RPC_URL`
- `MONAD_CONTRACT_ADDRESS` (still required as env var)

## Security Best Practices

### ✅ DO
- Use the keyring for storing sensitive credentials
- Keep your private keys secure and never share them
- Use the setup script to store credentials
- Regularly rotate your API keys

### ❌ DON'T
- Don't commit `.env` files with credentials to git
- Don't share your keyring credentials
- Don't store credentials in code or config files
- Don't log credential values in application logs

## Troubleshooting

### Issue: "Keyring is skipped due to an exception"

**Solution**: This was the original pip keyring problem. Fixed by running:
```bash
pip config set global.keyring-provider disabled
```

This disables pip's keyring provider (not your application's keyring usage).

### Issue: Credentials not found after setup

**Verify storage**:
```bash
python setup_credentials.py view
```

**Check keyring backend**:
```python
import keyring
print(keyring.get_keyring())
```

### Issue: Windows Credential Manager access denied

**Solution**: Run the application with appropriate Windows permissions. The Windows Credential Manager requires user-level permissions.

### Issue: Unicode/Emoji errors on Windows

**Fixed**: The setup script now automatically configures UTF-8 encoding for Windows consoles.

## Advanced Usage

### Programmatic Access

```python
from src.credential_manager import get_credential_manager, CredentialKey

# Get the credential manager
cred_mgr = get_credential_manager()

# Retrieve a credential
api_key = cred_mgr.get_credential(CredentialKey.ANTHROPIC_API_KEY)

# Store a credential
cred_mgr.set_credential(CredentialKey.MONAD_PRIVATE_KEY, "0x...")

# Check if credential exists
has_key = cred_mgr.has_credential(CredentialKey.MONAD_PRIVATE_KEY)

# Delete a credential
cred_mgr.delete_credential(CredentialKey.MONAD_PRIVATE_KEY)

# Validate all required credentials
all_present, missing = cred_mgr.validate_required_credentials()
```

### Custom Service Name

By default, credentials are stored under the service name `kinic-backend`. To use a custom service name:

```python
from src.credential_manager import CredentialManager

cred_mgr = CredentialManager(service_name="my-custom-service")
```

## Architecture

### Files Added

```
kinic-backend-windows/
├── src/
│   └── credential_manager.py       # Core credential management module
├── setup_credentials.py            # Interactive setup script
├── CREDENTIAL_SETUP.md            # This guide
└── requirements.txt               # Updated with keyring==25.6.0
```

### Code Changes

**src/main.py** (lines 37-59):
- Imports credential manager
- Loads credentials from keyring with environment variable fallback
- Updated error messages to reference setup script

**src/credential_manager.py**:
- `CredentialManager` class for keyring operations
- `CredentialKey` enum for type-safe credential references
- Logging for credential operations
- Automatic fallback to environment variables

**src/monad.py**:
- No changes required (already accepts credentials as parameters)

## Testing

### Test Credential Manager Import
```bash
python -c "from src.credential_manager import get_credential_manager; print('OK')"
```

### Test Setup Script
```bash
python setup_credentials.py help
python setup_credentials.py view
```

### Test Application Startup
```bash
# Set contract address
export MONAD_CONTRACT_ADDRESS=0xYourAddress

# Run application (will show credential loading logs)
python -m src.main
```

## Support

### Windows Credential Manager

View stored credentials:
1. Open Control Panel
2. Search for "Credential Manager"
3. Click "Windows Credentials"
4. Look for entries with "kinic-backend" in the name

### macOS Keychain

View stored credentials:
1. Open "Keychain Access" app
2. Search for "kinic-backend"
3. View or delete individual credentials

### Linux Secret Service

View stored credentials:
```bash
# Install seahorse (GNOME Keyring GUI)
sudo apt-get install seahorse

# Launch
seahorse
```

## FAQ

**Q: Are credentials encrypted?**
A: Yes, the OS keyring encrypts credentials using system-level encryption.

**Q: Can I still use environment variables?**
A: Yes, the application falls back to environment variables if credentials aren't in the keyring.

**Q: What happens if I delete credentials from the keyring?**
A: The application will fall back to environment variables, or fail with a clear error message if neither is available.

**Q: How do I backup my credentials?**
A: Backup your OS keyring using system-specific tools (Windows Backup, macOS Time Machine, etc.). For manual backup, export credentials to a secure password manager.

**Q: Can multiple applications share the same credentials?**
A: Yes, if they use the same service name ("kinic-backend"). You can also create separate service names for isolation.

---

**Last Updated**: 2025-11-16
**Version**: 1.0.0
**Status**: Production Ready
