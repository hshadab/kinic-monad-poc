#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Credential Setup Script for Kinic Backend

This script helps you securely store your credentials in the OS keyring
instead of using environment variables.

Credentials are stored in:
- Windows: Windows Credential Manager
- macOS: Keychain
- Linux: Secret Service API (freedesktop.org)
"""

import sys
import os
from getpass import getpass

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from credential_manager import get_credential_manager, CredentialKey


def print_header():
    """Print welcome header"""
    print("\n" + "="*70)
    print("🔐 Kinic Backend - Secure Credential Setup")
    print("="*70)
    print("\nThis script will help you securely store your credentials in the")
    print("operating system's keyring (Windows Credential Manager, macOS")
    print("Keychain, or Linux Secret Service).")
    print("\n" + "="*70 + "\n")


def print_section(title):
    """Print section header"""
    print(f"\n{'─'*70}")
    print(f"  {title}")
    print('─'*70)


def get_user_input(prompt, secret=False, optional=False, default=None):
    """
    Get user input with optional masking for secrets

    Args:
        prompt: The prompt to display
        secret: Whether to mask input (for passwords/keys)
        optional: Whether the field is optional
        default: Default value if input is empty

    Returns:
        User input string or None
    """
    optional_text = " (optional)" if optional else ""
    default_text = f" [default: {default}]" if default else ""
    full_prompt = f"{prompt}{optional_text}{default_text}: "

    if secret:
        value = getpass(full_prompt)
    else:
        value = input(full_prompt)

    # Handle empty input
    if not value:
        if default:
            return default
        elif optional:
            return None
        else:
            print("❌ This field is required!")
            return get_user_input(prompt, secret, optional, default)

    return value


def confirm_action(message):
    """Ask user to confirm an action"""
    response = input(f"{message} (y/n): ").lower().strip()
    return response in ['y', 'yes']


def setup_credentials():
    """Main setup function"""
    print_header()

    cred_mgr = get_credential_manager()

    # Check existing credentials
    print_section("Checking Existing Credentials")
    all_present, missing = cred_mgr.validate_required_credentials()

    if all_present:
        print("✅ All credentials are already configured in the keyring!")
        print("\nExisting credentials:")
        for key in CredentialKey:
            has_cred = cred_mgr.has_credential(key)
            status = "✓" if has_cred else "✗"
            print(f"  {status} {key.value}")

        if not confirm_action("\n⚠️  Do you want to update/replace existing credentials?"):
            print("\n👋 Setup cancelled. Your existing credentials remain unchanged.")
            return
    else:
        print(f"⚠️  Missing {len(missing)} credential(s):")
        for key in missing:
            print(f"  ✗ {key}")

    # Collect credentials
    print_section("Enter Your Credentials")
    print("\n💡 Tip: You can paste values (they won't be visible for secret fields)\n")

    credentials_to_set = {}

    # 1. Monad Private Key
    print("\n1️⃣  Monad Private Key")
    print("   This is your Ethereum private key for signing transactions on Monad.")
    monad_key = get_user_input("   Enter Monad private key (with or without 0x prefix)", secret=True)
    if monad_key and not monad_key.startswith('0x'):
        monad_key = '0x' + monad_key
    credentials_to_set[CredentialKey.MONAD_PRIVATE_KEY] = monad_key

    # 2. Anthropic API Key
    print("\n2️⃣  Anthropic API Key")
    print("   Get your API key from: https://console.anthropic.com/")
    anthropic_key = get_user_input("   Enter Anthropic API key", secret=True)
    credentials_to_set[CredentialKey.ANTHROPIC_API_KEY] = anthropic_key

    # 3. Kinic Memory ID
    print("\n3️⃣  Kinic Memory ID")
    print("   This is your Internet Computer canister memory ID.")
    memory_id = get_user_input("   Enter Kinic memory ID", secret=False)
    credentials_to_set[CredentialKey.KINIC_MEMORY_ID] = memory_id

    # 4. IC Identity Name (optional)
    print("\n4️⃣  Internet Computer Identity Name")
    print("   The DFX identity to use for IC operations.")
    identity = get_user_input("   Enter IC identity name", secret=False, optional=True, default="default")
    if identity:
        credentials_to_set[CredentialKey.IC_IDENTITY_NAME] = identity

    # 5. Monad RPC URL (optional)
    print("\n5️⃣  Monad RPC URL")
    print("   The RPC endpoint for Monad blockchain.")
    rpc_url = get_user_input("   Enter Monad RPC URL", secret=False, optional=True, default="https://testnet-rpc.monad.xyz")
    if rpc_url:
        credentials_to_set[CredentialKey.MONAD_RPC_URL] = rpc_url

    # Confirm before saving
    print_section("Review Your Configuration")
    print("\nThe following credentials will be saved to your OS keyring:\n")
    for key, value in credentials_to_set.items():
        # Mask sensitive values in display
        if "KEY" in key.value or "PRIVATE" in key.value:
            display_value = f"{value[:6]}...{value[-4:]}" if len(value) > 10 else "***"
        else:
            display_value = value
        print(f"  • {key.value}: {display_value}")

    print("\n⚠️  Note: MONAD_CONTRACT_ADDRESS must still be set as an environment variable.")

    if not confirm_action("\n✅ Save these credentials to your OS keyring?"):
        print("\n👋 Setup cancelled. No credentials were saved.")
        return

    # Save credentials
    print_section("Saving Credentials")
    success_count = 0
    for key, value in credentials_to_set.items():
        if cred_mgr.set_credential(key, value):
            print(f"  ✅ Saved: {key.value}")
            success_count += 1
        else:
            print(f"  ❌ Failed to save: {key.value}")

    # Summary
    print_section("Setup Complete")
    if success_count == len(credentials_to_set):
        print("\n🎉 All credentials saved successfully!\n")
        print("Your credentials are now securely stored in the OS keyring.")
        print("The application will automatically use them when it starts.\n")
        print("Next steps:")
        print("  1. Set MONAD_CONTRACT_ADDRESS environment variable")
        print("  2. Run your Kinic backend: python -m src.main")
    else:
        print(f"\n⚠️  Saved {success_count}/{len(credentials_to_set)} credentials.")
        print("Some credentials failed to save. Please try again.")

    print("\n" + "="*70 + "\n")


def view_credentials():
    """View stored credentials (masked)"""
    print_header()
    print_section("Stored Credentials")

    cred_mgr = get_credential_manager()

    print("\nCredentials in your OS keyring:\n")
    for key in CredentialKey:
        value = cred_mgr.get_credential(key)
        if value:
            # Mask sensitive values
            if "KEY" in key.value or "PRIVATE" in key.value:
                display_value = f"{value[:6]}...{value[-4:]}" if len(value) > 10 else "***"
            else:
                display_value = value
            print(f"  ✅ {key.value}: {display_value}")
        else:
            print(f"  ❌ {key.value}: Not set")

    print("\n" + "="*70 + "\n")


def delete_credentials():
    """Delete all stored credentials"""
    print_header()
    print_section("Delete Credentials")

    print("\n⚠️  This will DELETE all Kinic credentials from your OS keyring!")
    if not confirm_action("\n❗ Are you sure you want to delete ALL credentials?"):
        print("\n👋 Deletion cancelled.")
        return

    print("\n🗑️  Deleting credentials...\n")
    cred_mgr = get_credential_manager()

    deleted_count = 0
    for key in CredentialKey:
        if cred_mgr.delete_credential(key):
            print(f"  ✅ Deleted: {key.value}")
            deleted_count += 1

    print(f"\n✅ Deleted {deleted_count} credential(s).")
    print("\n" + "="*70 + "\n")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command in ['view', 'list', 'show']:
            view_credentials()
        elif command in ['delete', 'remove', 'clear']:
            delete_credentials()
        elif command in ['help', '-h', '--help']:
            print("\nUsage:")
            print("  python setup_credentials.py          # Interactive setup")
            print("  python setup_credentials.py view     # View stored credentials")
            print("  python setup_credentials.py delete   # Delete all credentials")
            print("  python setup_credentials.py help     # Show this help\n")
        else:
            print(f"\n❌ Unknown command: {command}")
            print("Run 'python setup_credentials.py help' for usage.\n")
    else:
        setup_credentials()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
