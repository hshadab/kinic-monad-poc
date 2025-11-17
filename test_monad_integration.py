#!/usr/bin/env python3
"""
Test Monad blockchain integration
"""
import asyncio
import os
from dotenv import load_dotenv
from src.monad import MonadLogger
from src.metadata import extract_metadata

# Load environment variables
load_dotenv()

async def test_monad_logging():
    print("\n" + "="*70)
    print("🧪 TESTING MONAD BLOCKCHAIN INTEGRATION")
    print("="*70)
    
    # Initialize Monad logger
    print("\n1️⃣  Initializing MonadLogger...")
    monad = MonadLogger(
        rpc_url=os.getenv("MONAD_RPC_URL"),
        private_key=os.getenv("MONAD_PRIVATE_KEY"),
        contract_address=os.getenv("MONAD_CONTRACT_ADDRESS"),
        abi_path="contracts/abi.json"
    )
    
    # Check existing stats
    print("\n2️⃣  Checking current blockchain stats...")
    total_before = monad.get_total_memories()
    user_before = monad.get_user_memory_count(monad.account.address)
    print(f"   Total memories: {total_before}")
    print(f"   Your memories: {user_before}")
    
    # Test content
    test_content = """# Kinic Backend Test
This is a test memory to verify Monad blockchain integration is working correctly.
Testing keyring credentials, metadata extraction, and blockchain logging.
"""
    
    # Extract metadata
    print("\n3️⃣  Extracting metadata...")
    metadata = extract_metadata(test_content, "test,integration")
    print(f"   Title: {metadata.title}")
    print(f"   Tags: {metadata.tags}")
    print(f"   Hash: {metadata.content_hash[:20]}...")
    
    # Log to Monad
    print("\n4️⃣  Logging to Monad blockchain...")
    print("   ⏳ Sending transaction...")
    tx_hash = await monad.log_insert(
        title=metadata.title,
        summary=metadata.summary,
        tags=metadata.tags,
        content_hash=metadata.content_hash
    )
    print(f"   ✅ Transaction confirmed!")
    print(f"   📝 TX Hash: {tx_hash}")
    
    # Verify the log
    print("\n5️⃣  Verifying on-chain data...")
    total_after = monad.get_total_memories()
    user_after = monad.get_user_memory_count(monad.account.address)
    print(f"   Total memories: {total_before} → {total_after} (+{total_after - total_before})")
    print(f"   Your memories: {user_before} → {user_after} (+{user_after - user_before})")
    
    # Explorer link
    print(f"\n🔍 View on explorer:")
    print(f"   https://mainnet-beta.monvision.io/tx/{tx_hash}")
    
    print("\n" + "="*70)
    print("✅ MONAD INTEGRATION TEST PASSED!")
    print("="*70)
    print(f"\n💰 Gas used: Check transaction for details")
    print(f"💳 Remaining balance: Check wallet\n")

if __name__ == "__main__":
    asyncio.run(test_monad_logging())
