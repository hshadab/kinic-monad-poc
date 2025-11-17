#!/usr/bin/env python3
"""
Deploy KinicMemoryLog contract to Monad network
"""
import os
import json
from web3 import Web3
from eth_account import Account
from solcx import compile_source, install_solc

def compile_contract():
    """Compile the Solidity contract"""
    print("📦 Compiling KinicMemoryLog.sol...")

    with open("contracts/KinicMemoryLog.sol", "r") as f:
        source = f.read()

    # Install solc if needed
    try:
        install_solc("0.8.20")
    except:
        pass

    compiled = compile_source(
        source,
        output_values=["abi", "bin"],
        solc_version="0.8.20"
    )

    contract_id, contract_interface = compiled.popitem()

    return contract_interface["abi"], contract_interface["bin"]

def deploy_contract(rpc_url, private_key):
    """Deploy contract to Monad"""
    print(f"🔗 Connecting to Monad at {rpc_url}...")

    w3 = Web3(Web3.HTTPProvider(rpc_url))

    if not w3.is_connected():
        raise Exception("Failed to connect to Monad RPC")

    print(f"✅ Connected! Chain ID: {w3.eth.chain_id}")

    # Get account
    account = Account.from_key(private_key)
    print(f"📝 Deploying from: {account.address}")

    # Get balance
    balance = w3.eth.get_balance(account.address)
    print(f"💰 Balance: {w3.from_wei(balance, 'ether')} ETH")

    if balance == 0:
        print("⚠️  WARNING: Account has 0 balance!")

    # Compile
    abi, bytecode = compile_contract()

    # Create contract
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Build transaction
    print("🚀 Building deployment transaction...")
    txn = Contract.constructor().build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price
    })

    # Sign and send
    print("✍️  Signing transaction...")
    signed = account.sign_transaction(txn)

    print("📡 Sending transaction...")
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"📋 Transaction hash: {tx_hash.hex()}")

    # Wait for receipt
    print("⏳ Waiting for confirmation...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    if receipt['status'] == 1:
        print(f"✅ Contract deployed successfully!")
        print(f"📍 Contract address: {receipt['contractAddress']}")

        # Save ABI
        with open("contracts/abi.json", "w") as f:
            json.dump(abi, f, indent=2)
        print("💾 ABI saved to contracts/abi.json")

        # Save deployment info
        deployment_info = {
            "contract_address": receipt['contractAddress'],
            "deployer": account.address,
            "tx_hash": tx_hash.hex(),
            "block_number": receipt['blockNumber'],
            "gas_used": receipt['gasUsed'],
            "network": rpc_url
        }

        with open("contracts/deployment.json", "w") as f:
            json.dump(deployment_info, f, indent=2)
        print("💾 Deployment info saved to contracts/deployment.json")

        return receipt['contractAddress']
    else:
        raise Exception("Deployment failed!")

if __name__ == "__main__":
    # Load from environment
    rpc_url = os.getenv("MONAD_RPC_URL", "https://testnet-rpc.monad.xyz")
    private_key = os.getenv("MONAD_PRIVATE_KEY")

    if not private_key:
        print("❌ Error: MONAD_PRIVATE_KEY environment variable not set")
        print("Usage: MONAD_PRIVATE_KEY=0x... python contracts/deploy.py")
        exit(1)

    try:
        contract_address = deploy_contract(rpc_url, private_key)
        print("\n" + "="*60)
        print("🎉 DEPLOYMENT COMPLETE!")
        print("="*60)
        print(f"Contract Address: {contract_address}")
        print(f"\nAdd this to your .env file:")
        print(f"MONAD_CONTRACT_ADDRESS={contract_address}")
        print("="*60)
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        exit(1)
