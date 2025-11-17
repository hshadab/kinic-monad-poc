#!/usr/bin/env python3
"""
Generate a new Ethereum wallet for Monad deployment
"""
import sys
sys.path.insert(0, '../venv/lib/python3.12/site-packages')

from eth_account import Account
import secrets

def generate_wallet():
    """Generate a new Ethereum wallet"""

    # Generate random private key
    private_key = "0x" + secrets.token_hex(32)

    # Create account from private key
    account = Account.from_key(private_key)

    print("\n" + "="*70)
    print("🔑 NEW MONAD WALLET GENERATED")
    print("="*70)
    print("\n⚠️  SAVE THESE CREDENTIALS SECURELY - THEY CANNOT BE RECOVERED!")
    print("\n" + "-"*70)
    print(f"\n📍 Address:     {account.address}")
    print(f"\n🔐 Private Key: {private_key}")
    print("\n" + "-"*70)
    print("\n📝 Next Steps:")
    print("\n1. SAVE the private key in a secure location (password manager)")
    print(f"\n2. Fund this address with Monad tokens:")
    print(f"   → Send tokens to: {account.address}")
    print(f"   → Or use Monad faucet if available")
    print("\n3. This wallet will be used to:")
    print("   ✓ Deploy the KinicMemoryLog smart contract")
    print("   ✓ Sign transactions for memory operations")
    print("   ✓ Pay gas fees on Monad")
    print("\n4. I'll add the private key to your .env file")
    print("\n" + "="*70)
    print("\n⚠️  SECURITY WARNINGS:")
    print("   • Never share your private key")
    print("   • Never commit it to git (already in .gitignore)")
    print("   • Store it in Render dashboard as a secret env var")
    print("   • Consider using a hardware wallet for production")
    print("\n" + "="*70 + "\n")

    return private_key, account.address

if __name__ == "__main__":
    generate_wallet()
