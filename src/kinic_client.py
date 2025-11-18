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
                    json={"markdown": text},  # API expects "markdown" field
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()

                # API returns {"chunks": [{"sentence": "...", "embedding": [...]}]}
                chunks = data.get("chunks", [])
                if not chunks:
                    return []

                # Extract embeddings from chunks
                embeddings = [chunk["embedding"] for chunk in chunks if "embedding" in chunk]
                return embeddings

        except Exception as e:
            print(f"Embedding API error: {e}")
            import traceback
            traceback.print_exc()
            # Return empty list on error
            return []

    async def insert(self, content: str, tag: str = "general", principal: str = None) -> Dict:
        """
        Insert content into Kinic memory via IC

        Canister method: insert(vec float32, text) -> nat32

        Args:
            content: Text content to store
            tag: Tag to associate with content (used in text)
            principal: Internet Identity principal for user isolation (optional)

        Returns:
            Result dictionary
        """
        try:
            # 1. Get embedding from Kinic API
            print(f"Getting embedding for {len(content)} chars...")
            embeddings = await self.get_embeddings(content)

            if not embeddings or len(embeddings) == 0:
                return {
                    "status": "error",
                    "error": "Failed to generate embeddings",
                    "tag": tag
                }

            # Use first embedding vector (late-chunking should return one vector per text)
            embedding_vector = embeddings[0]
            print(f"Got embedding vector of length {len(embedding_vector)}")

            # 2. Prepare text with tag (prepend principal for user isolation)
            if principal:
                final_tag = f"{principal}|{tag}"
                print(f"Using principal-scoped tag: {final_tag[:50]}...")
            else:
                final_tag = tag

            tagged_text = f"{final_tag}: {content}"

            # 3. Encode arguments: (vec float32, text)
            # ic-py candid encoding
            params = [
                {'type': Types.Vec(Types.Float32), 'value': embedding_vector},
                {'type': Types.Text, 'value': tagged_text}
            ]

            # 4. Call IC canister insert method
            print(f"Calling canister {self.memory_id} insert method...")
            result = await self.agent.update_raw(
                self.memory_id,
                "insert",
                encode(params)
            )

            # Decode response (nat32 = memory ID)
            memory_id = decode(result, [{'type': Types.Nat32}])[0]

            print(f"Successfully inserted memory ID: {memory_id}")

            return {
                "status": "inserted",
                "memory_id": memory_id,
                "embedding_dim": len(embedding_vector),
                "tag": final_tag
            }

        except Exception as e:
            print(f"Insert error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e),
                "tag": tag
            }

    async def search(self, query: str, top_k: int = 5, principal: str = None) -> List[Dict]:
        """
        Search Kinic memory via IC

        Canister method: search(vec float32) -> vec record { float32; text }

        Args:
            query: Search query string
            top_k: Number of results (note: canister returns all, we filter)
            principal: Internet Identity principal for user isolation (optional)

        Returns:
            List of search results with score and text
        """
        try:
            # 1. Get query embedding
            print(f"Getting embedding for query: {query[:50]}...")
            embeddings = await self.get_embeddings(query)

            if not embeddings or len(embeddings) == 0:
                print("Failed to get query embedding")
                return []

            query_embedding = embeddings[0]
            print(f"Got query embedding of length {len(query_embedding)}")

            # 2. Encode search argument: vec float32
            params = [
                {'type': Types.Vec(Types.Float32), 'value': query_embedding}
            ]

            # 3. Call IC canister search method (query, not update)
            print(f"Calling canister {self.memory_id} search method...")
            result = await self.agent.query_raw(
                self.memory_id,
                "search",
                encode(params)
            )

            # 4. Decode response: vec record { float32; text }
            # ic-py should decode this as list of tuples
            search_results = decode(result, [
                {'type': Types.Vec(
                    Types.Record([
                        {'type': Types.Float32},
                        {'type': Types.Text}
                    ])
                )}
            ])[0]

            print(f"Got {len(search_results)} search results from canister")

            # 5. Format results and filter by principal if provided
            formatted_results = []
            for score, text in search_results:
                # Extract tag if present
                tag = ""
                if ":" in text:
                    tag, text = text.split(":", 1)
                    text = text.strip()

                tag = tag.strip()

                # Filter by principal if provided
                if principal:
                    # Check if tag starts with principal (format: "principal|actualtag")
                    if not tag.startswith(f"{principal}|"):
                        continue  # Skip this result, doesn't match user's principal

                    # Extract actual tag after principal prefix
                    if "|" in tag:
                        _, actual_tag = tag.split("|", 1)
                        tag = actual_tag

                formatted_results.append({
                    "score": float(score),
                    "text": text,
                    "tag": tag
                })

                # Limit to top_k after filtering
                if len(formatted_results) >= top_k:
                    break

            if principal:
                print(f"Filtered to {len(formatted_results)} results for principal {principal[:10]}...")
            else:
                print(f"Returning {len(formatted_results)} results (no principal filter)")

            return formatted_results

        except Exception as e:
            print(f"Search error: {e}")
            import traceback
            traceback.print_exc()
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
