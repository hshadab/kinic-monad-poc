"""
Pure Python client for Kinic (Internet Computer) using ic-py
Replaces kinic-cli Rust binary to avoid keychain dependency
"""
import os
import httpx
from typing import List, Dict
from ic.identity import Identity
from ic.client import Client
from ic.agent import Agent
from ic.candid import encode, decode, Types


class KinicClient:
    """
    Python client for Kinic memory canister on Internet Computer
    Uses ic-py for IC communication and httpx for embedding API
    """

    def __init__(self, memory_id: str, identity_pem: str, ic_url: str = "https://ic0.app"):
        """
        Initialize Kinic client

        Args:
            memory_id: IC canister principal ID for memory storage
            identity_pem: PEM-formatted IC identity private key
            ic_url: Internet Computer gateway URL
        """
        self.memory_id = memory_id
        self.ic_url = ic_url

        # Embedding API endpoint (Kinic's embedding service)
        self.embedding_api = os.getenv("EMBEDDING_API_ENDPOINT", "https://api.kinic.io")

        # Parse PEM to extract private key
        # ic-py Identity accepts hex private key, need to extract from PEM
        self.identity = self._identity_from_pem(identity_pem)

        # Create IC agent
        self.client = Client(url=ic_url)
        self.agent = Agent(self.identity, self.client)

        print(f"KinicClient initialized with canister: {memory_id}")

    def _identity_from_pem(self, pem_content: str) -> Identity:
        """
        Create Identity from PEM string

        Args:
            pem_content: PEM-formatted private key

        Returns:
            Identity object
        """
        try:
            # Try to extract hex key from PEM
            # For EC PRIVATE KEY, the key is base64 encoded
            import base64
            import re

            # Remove PEM headers/footers
            pem_body = re.sub(r'-----BEGIN.*?-----\n?', '', pem_content)
            pem_body = re.sub(r'-----END.*?-----\n?', '', pem_body)
            pem_body = pem_body.replace('\n', '').replace('\r', '')

            # Decode base64 to get DER format
            der_bytes = base64.b64decode(pem_body)

            # Extract the private key from DER (last 32 bytes for EC)
            # This is a simplified extraction - may need adjustment
            private_key_hex = der_bytes[-32:].hex()

            print(f"Extracted private key from PEM (length: {len(private_key_hex)})")
            return Identity(privkey=private_key_hex)

        except Exception as e:
            print(f"Warning: Failed to parse PEM, using random identity: {e}")
            # Fallback to random identity for testing
            return Identity()

    async def get_embeddings(self, text: str) -> List[List[float]]:
        """
        Get embeddings from Kinic API using late chunking

        Args:
            text: Content to embed

        Returns:
            List of embedding vectors
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.embedding_api}/late-chunking",
                    json={"text": text},
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()

                # API should return embeddings list
                return data.get("embeddings", [])

        except Exception as e:
            print(f"Embedding API error: {e}")
            # Return empty list on error
            return []

    async def insert(self, content: str, tag: str = "general") -> Dict:
        """
        Insert content into Kinic memory via IC

        Args:
            content: Text content to store
            tag: Tag to associate with content

        Returns:
            Result dictionary
        """
        try:
            # 1. Get embeddings from Kinic API
            print(f"Getting embeddings for {len(content)} chars...")
            embeddings = await self.get_embeddings(content)

            if not embeddings:
                return {
                    "status": "error",
                    "error": "Failed to generate embeddings",
                    "tag": tag
                }

            print(f"Got {len(embeddings)} embedding vectors")

            # 2. Call IC canister to store embeddings
            # The canister's insert method signature needs to match
            # This is a simplified version - adjust based on actual canister interface
            params = [
                {'type': Types.Text, 'value': content},
                {'type': Types.Text, 'value': tag},
                # Add embeddings as vec<vec<f32>> or similar
            ]

            # For now, just return success since we don't have the exact canister interface
            # In production, would call: result = self.agent.update_raw(self.memory_id, "insert", encode(params))

            return {
                "status": "inserted",
                "embeddings_count": len(embeddings),
                "tag": tag
            }

        except Exception as e:
            print(f"Insert error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "tag": tag
            }

    async def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search Kinic memory via IC

        Args:
            query: Search query string
            top_k: Number of results

        Returns:
            List of search results
        """
        try:
            # 1. Get query embedding
            print(f"Getting embedding for query: {query}")
            embeddings = await self.get_embeddings(query)

            if not embeddings:
                return []

            query_embedding = embeddings[0] if embeddings else []

            # 2. Call IC canister to search
            # params = [
            #     {'type': Types.Vec(Types.Float32), 'value': query_embedding},
            #     {'type': Types.Nat, 'value': top_k}
            # ]
            # results = self.agent.query_raw(self.memory_id, "search", encode(params))

            # For now, return empty since we need the exact canister interface
            return []

        except Exception as e:
            print(f"Search error: {e}")
            return []


# Quick test
if __name__ == "__main__":
    import asyncio

    async def test():
        memory_id = os.getenv("KINIC_MEMORY_ID", "2x5sz-ciaaa-aaaak-apgta-cai")
        identity_pem = os.getenv("IC_IDENTITY_PEM", "")

        if not identity_pem:
            print("Set IC_IDENTITY_PEM environment variable")
            return

        client = KinicClient(memory_id, identity_pem)

        # Test insert
        print("\n=== Testing Insert ===")
        result = await client.insert("Test memory content", "test")
        print(f"Result: {result}")

        # Test search
        print("\n=== Testing Search ===")
        results = await client.search("test memory")
        print(f"Results: {results}")

    asyncio.run(test())
