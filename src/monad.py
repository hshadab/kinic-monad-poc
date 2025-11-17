"""
Monad blockchain connector for logging memory metadata
"""
import os
import json
from pathlib import Path
from web3 import Web3
from eth_account import Account
from typing import Optional


class MonadLogger:
    """
    Interface to KinicMemoryLog smart contract on Monad
    Logs rich metadata about memory operations
    """

    def __init__(
        self,
        rpc_url: str,
        private_key: str,
        contract_address: str,
        abi_path: str = "contracts/abi.json"
    ):
        """
        Initialize Monad logger

        Args:
            rpc_url: Monad RPC endpoint
            private_key: Private key for signing transactions
            contract_address: Deployed KinicMemoryLog contract address
            abi_path: Path to contract ABI JSON file
        """
        print(f" Connecting to Monad at {rpc_url}...")

        # Configure HTTP provider with timeout for Windows compatibility
        from web3.providers import HTTPProvider
        provider = HTTPProvider(
            rpc_url,
            request_kwargs={'timeout': 30}  # 30 second timeout
        )
        self.w3 = Web3(provider)

        try:
            if not self.w3.is_connected():
                raise Exception(f"Failed to connect to Monad at {rpc_url}")
        except Exception as e:
            print(f" Connection error: {str(e)}")
            print(f"   This may be a Windows Firewall or SSL certificate issue")
            raise Exception(f"Failed to connect to Monad at {rpc_url}: {str(e)}")

        print(f" Connected to Monad! Chain ID: {self.w3.eth.chain_id}")

        # Set up account
        self.account = Account.from_key(private_key)
        print(f" Using account: {self.account.address}")

        # Load contract ABI
        abi_full_path = Path(abi_path)
        if not abi_full_path.exists():
            raise FileNotFoundError(f"ABI file not found at {abi_path}")

        with open(abi_full_path) as f:
            abi = json.load(f)

        # Initialize contract
        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=abi
        )

        print(f" Contract loaded at: {contract_address}")

    async def log_insert(
        self,
        title: str,
        summary: str,
        tags: str,
        content_hash: str
    ) -> str:
        """
        Log memory insertion to Monad

        Args:
            title: Memory title
            summary: Content summary
            tags: Comma-separated tags
            content_hash: SHA256 hash of content (with 0x prefix)

        Returns:
            Transaction hash
        """
        return await self._log_memory(0, title, summary, tags, content_hash)

    async def log_search(
        self,
        title: str,
        summary: str,
        tags: str,
        content_hash: str
    ) -> str:
        """
        Log search operation to Monad

        Args:
            title: Search title/query
            summary: Query summary
            tags: Search tags
            content_hash: Hash of query

        Returns:
            Transaction hash
        """
        return await self._log_memory(1, title, summary, tags, content_hash)

    async def _log_memory(
        self,
        op_type: int,
        title: str,
        summary: str,
        tags: str,
        content_hash: str
    ) -> str:
        """
        Internal method to log memory to Monad

        Args:
            op_type: 0=INSERT, 1=SEARCH
            title: Title (max 100 chars)
            summary: Summary (max 200 chars)
            tags: Comma-separated tags
            content_hash: Content hash (0x-prefixed hex string)

        Returns:
            Transaction hash
        """
        # Validate inputs
        if len(title) > 100:
            title = title[:97] + "..."
        if len(summary) > 200:
            summary = summary[:197] + "..."

        # Convert hash to bytes32
        if content_hash.startswith("0x"):
            content_hash = content_hash[2:]

        content_hash_bytes = bytes.fromhex(content_hash)

        print(f" Logging to Monad: opType={op_type}, title='{title[:30]}...'")

        # Build transaction
        try:
            txn = self.contract.functions.logMemory(
                op_type,
                title,
                summary,
                tags,
                content_hash_bytes
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 300000,  # Increased for string storage
                'gasPrice': self.w3.eth.gas_price
            })
        except Exception as e:
            print(f" Error building transaction: {e}")
            raise

        # Sign transaction
        signed = self.account.sign_transaction(txn)

        # Send transaction
        try:
            tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
            print(f" Transaction sent: {tx_hash.hex()}")
        except Exception as e:
            print(f" Error sending transaction: {e}")
            raise

        # Wait for receipt
        try:
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

            if receipt['status'] == 1:
                print(f" Transaction confirmed! Block: {receipt['blockNumber']}")
                return tx_hash.hex()
            else:
                raise Exception("Transaction failed")

        except Exception as e:
            print(f"  Transaction may still be pending: {e}")
            # Return hash even if receipt fails (can check later)
            return tx_hash.hex()

    def get_memory(self, memory_id: int) -> dict:
        """
        Retrieve memory metadata from Monad

        Args:
            memory_id: On-chain memory ID

        Returns:
            Memory struct as dict
        """
        memory = self.contract.functions.getMemory(memory_id).call()

        return {
            "user": memory[0],
            "opType": memory[1],
            "title": memory[2],
            "summary": memory[3],
            "tags": memory[4],
            "contentHash": "0x" + memory[5].hex(),
            "timestamp": memory[6]
        }

    def get_user_memory_count(self, user_address: str) -> int:
        """Get number of memories for a user"""
        return self.contract.functions.getUserMemoryCount(
            Web3.to_checksum_address(user_address)
        ).call()

    def get_total_memories(self) -> int:
        """Get total number of memories logged"""
        return self.contract.functions.getTotalMemories().call()


# Quick test
if __name__ == "__main__":
    import asyncio

    async def test():
        rpc_url = os.getenv("MONAD_RPC_URL", "https://testnet-rpc.monad.xyz")
        private_key = os.getenv("MONAD_PRIVATE_KEY")
        contract_address = os.getenv("MONAD_CONTRACT_ADDRESS")

        if not private_key or not contract_address:
            print(" Set MONAD_PRIVATE_KEY and MONAD_CONTRACT_ADDRESS env vars")
            return

        logger = MonadLogger(rpc_url, private_key, contract_address)

        # Test logging
        tx = await logger.log_insert(
            title="Test Memory",
            summary="This is a test memory from the Monad logger",
            tags="test,example",
            content_hash="0x" + "a" * 64
        )

        print(f"\n Test transaction: {tx}")

        # Get stats
        total = logger.get_total_memories()
        print(f" Total memories on-chain: {total}")

    asyncio.run(test())
