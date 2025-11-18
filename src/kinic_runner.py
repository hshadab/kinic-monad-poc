"""
Wrapper for kinic_py package to interact with Internet Computer
Uses Python bindings (PyO3) for direct interaction with IC memory canisters
"""
import asyncio
from typing import List, Dict, Tuple
from kinic_py import KinicMemories


class KinicRunner:
    """
    Manages Kinic memory operations via kinic_py package (Python bindings)
    """

    def __init__(self, memory_id: str, identity: str, ic: bool = True):
        """
        Initialize Kinic runner

        Args:
            memory_id: IC canister principal ID for memory storage
            identity: IC identity name to use (e.g., "default")
            ic: If True, connect to IC mainnet; if False, use local replica
        """
        self.memory_id = memory_id
        self.identity = identity
        self.ic = ic

        # Initialize KinicMemories instance
        self.km = KinicMemories(identity, ic=ic)

        print(f"KinicRunner initialized:")
        print(f"  - Identity: {self.identity}")
        print(f"  - Memory ID: {self.memory_id}")
        print(f"  - Network: {'IC Mainnet' if self.ic else 'Local Replica'}")

    async def insert(self, content: str, tag: str = "general") -> Dict:
        """
        Insert content into Kinic memory via IC

        Args:
            content: Text content to store
            tag: Tag to associate with content

        Returns:
            Result dictionary with status and chunk count
        """
        try:
            # Run kinic_py insert in thread pool to avoid blocking event loop
            loop = asyncio.get_event_loop()
            chunks_inserted = await loop.run_in_executor(
                None,
                self.km.insert_text,
                self.memory_id,
                tag,
                content
            )

            return {
                "status": "inserted",
                "chunks": chunks_inserted,
                "tag": tag,
                "memory_id": self.memory_id
            }

        except Exception as e:
            print(f"Error inserting content: {e}")
            raise RuntimeError(f"Failed to insert content into Kinic: {str(e)}")

    async def search(self, query: str, format: str = "json", top_k: int = 5) -> List[Dict]:
        """
        Search Kinic memory via IC

        Args:
            query: Search query string
            format: Output format (json, text, csv) - kept for API compatibility
            top_k: Number of top results to return

        Returns:
            List of search results with scores and text
        """
        try:
            # Run kinic_py search in thread pool to avoid blocking event loop
            loop = asyncio.get_event_loop()
            results: List[Tuple[float, str]] = await loop.run_in_executor(
                None,
                self.km.search,
                self.memory_id,
                query
            )

            # Convert to dictionary format and apply top_k limit
            formatted_results = [
                {
                    "score": float(score),
                    "text": text,
                    "sentence": text,  # Alias for compatibility
                    "tag": None  # Tag not returned by search, could be enhanced
                }
                for score, text in results[:top_k]
            ]

            return formatted_results

        except Exception as e:
            print(f"Error searching Kinic: {e}")
            raise RuntimeError(f"Failed to search Kinic memories: {str(e)}")

    async def list_memories(self) -> Dict:
        """
        List all deployed memory canisters for this identity

        Returns:
            Dictionary with list of memory canister IDs
        """
        try:
            # Run kinic_py list in thread pool to avoid blocking event loop
            loop = asyncio.get_event_loop()
            memories: List[str] = await loop.run_in_executor(
                None,
                self.km.list
            )

            return {
                "status": "success",
                "memories": memories,
                "count": len(memories)
            }

        except Exception as e:
            print(f"Error listing memories: {e}")
            raise RuntimeError(f"Failed to list Kinic memories: {str(e)}")

    async def create_memory(self, name: str, description: str) -> str:
        """
        Create a new memory canister

        Args:
            name: Name for the new memory
            description: Description of the memory

        Returns:
            Canister ID of the newly created memory
        """
        try:
            # Run kinic_py create in thread pool to avoid blocking event loop
            loop = asyncio.get_event_loop()
            canister_id: str = await loop.run_in_executor(
                None,
                self.km.create,
                name,
                description
            )

            return canister_id

        except Exception as e:
            print(f"Error creating memory: {e}")
            raise RuntimeError(f"Failed to create Kinic memory: {str(e)}")


# Quick test
if __name__ == "__main__":
    import os
    import json

    async def test():
        """Test KinicRunner with kinic_py bindings"""
        # Test with environment variables
        memory_id = os.getenv("KINIC_MEMORY_ID", "test-canister-id")
        identity = os.getenv("IC_IDENTITY_NAME", "default")

        print("\n" + "="*60)
        print("Testing KinicRunner with Python Bindings")
        print("="*60)

        try:
            runner = KinicRunner(memory_id, identity, ic=True)

            # Test insert
            print("\n=== Testing Insert ===")
            result = await runner.insert(
                "# Test Memory\nThis is a test memory using kinic_py bindings.",
                "test"
            )
            print(json.dumps(result, indent=2))

            # Test search
            print("\n=== Testing Search ===")
            results = await runner.search("test memory", top_k=5)
            print(f"Found {len(results)} results:")
            print(json.dumps(results, indent=2))

            # Test list
            print("\n=== Testing List Memories ===")
            memories = await runner.list_memories()
            print(json.dumps(memories, indent=2))

            print("\n" + "="*60)
            print("All tests completed successfully!")
            print("="*60)

        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()

    asyncio.run(test())
