"""
Monad Cache - Local caching and search for Monad blockchain metadata
Enables fast querying of on-chain memory logs without gas costs
"""
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from collections import defaultdict


class MonadCache:
    """
    In-memory cache of Monad blockchain memory logs
    Provides fast search capabilities over on-chain metadata
    """

    def __init__(self, monad_logger):
        """
        Initialize cache with MonadLogger instance

        Args:
            monad_logger: MonadLogger instance for blockchain queries
        """
        self.monad = monad_logger
        self.memories: List[Dict] = []
        self.tag_index: Dict[str, List[int]] = defaultdict(list)
        self.user_index: Dict[str, List[int]] = defaultdict(list)
        self.synced = False
        self.last_sync = None

    async def sync_from_blockchain(self):
        """
        Sync all memories from Monad blockchain
        Builds local cache and indices for fast search
        """
        print("\n🔄 Syncing Monad cache from blockchain...")

        try:
            # Get total memories from blockchain
            total = self.monad.get_total_memories()
            print(f"   Found {total} memories on-chain")

            if total == 0:
                print("   No memories to sync yet")
                self.synced = True
                self.last_sync = datetime.now()
                return

            # Fetch all memories (run in executor for blocking calls)
            loop = asyncio.get_event_loop()

            def _fetch_all():
                memories = []
                for i in range(total):
                    try:
                        memory = self.monad.get_memory(i)
                        memory['id'] = i  # Add ID
                        memories.append(memory)
                    except Exception as e:
                        print(f"   Warning: Failed to fetch memory {i}: {e}")
                        continue
                return memories

            self.memories = await loop.run_in_executor(None, _fetch_all)

            # Build indices for fast search
            self._build_indices()

            self.synced = True
            self.last_sync = datetime.now()

            print(f"✅ Monad cache synced: {len(self.memories)} memories indexed")
            print(f"   Unique tags: {len(self.tag_index)}")
            print(f"   Users: {len(self.user_index)}")

        except Exception as e:
            print(f"❌ Failed to sync Monad cache: {e}")
            import traceback
            traceback.print_exc()

    def _build_indices(self):
        """Build search indices for tags and users"""
        self.tag_index.clear()
        self.user_index.clear()

        for i, memory in enumerate(self.memories):
            # Index by tags
            tags = memory.get('tags', '').lower()
            if tags:
                for tag in tags.split(','):
                    tag = tag.strip()
                    if tag:
                        self.tag_index[tag].append(i)

            # Index by user
            user = memory.get('user', '').lower()
            if user:
                self.user_index[user].append(i)

    def search_by_tags(
        self,
        tag_query: str,
        limit: int = 50,
        op_type: Optional[int] = None
    ) -> List[Dict]:
        """
        Search memories by tags

        Args:
            tag_query: Comma-separated tags or single tag
            limit: Maximum results to return
            op_type: Filter by operation type (0=INSERT, 1=SEARCH)

        Returns:
            List of matching memories
        """
        if not self.synced:
            return []

        # Parse query tags
        query_tags = [t.strip().lower() for t in tag_query.split(',')]

        # Find memories with ANY matching tag
        matching_ids = set()
        for tag in query_tags:
            if tag in self.tag_index:
                matching_ids.update(self.tag_index[tag])

        # Filter by op_type if specified
        results = []
        for memory_id in matching_ids:
            memory = self.memories[memory_id]

            if op_type is not None and memory['opType'] != op_type:
                continue

            results.append(memory)

            if len(results) >= limit:
                break

        # Sort by timestamp (most recent first)
        results.sort(key=lambda m: m['timestamp'], reverse=True)

        return results

    def search_by_title(
        self,
        query: str,
        limit: int = 50,
        op_type: Optional[int] = None
    ) -> List[Dict]:
        """
        Search memories by title (case-insensitive substring match)

        Args:
            query: Search query
            limit: Maximum results
            op_type: Filter by operation type

        Returns:
            List of matching memories
        """
        if not self.synced:
            return []

        query_lower = query.lower()
        results = []

        for memory in self.memories:
            # Filter by op_type
            if op_type is not None and memory['opType'] != op_type:
                continue

            # Check title match
            title = memory.get('title', '').lower()
            if query_lower in title:
                results.append(memory)

                if len(results) >= limit:
                    break

        # Sort by timestamp (most recent first)
        results.sort(key=lambda m: m['timestamp'], reverse=True)

        return results

    def search_by_summary(
        self,
        query: str,
        limit: int = 50
    ) -> List[Dict]:
        """
        Search memories by summary content

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of matching memories
        """
        if not self.synced:
            return []

        query_lower = query.lower()
        results = []

        for memory in self.memories:
            summary = memory.get('summary', '').lower()
            if query_lower in summary:
                results.append(memory)

                if len(results) >= limit:
                    break

        # Sort by timestamp (most recent first)
        results.sort(key=lambda m: m['timestamp'], reverse=True)

        return results

    def get_recent(
        self,
        limit: int = 20,
        op_type: Optional[int] = None
    ) -> List[Dict]:
        """
        Get most recent memories

        Args:
            limit: Number of memories to return
            op_type: Filter by operation type

        Returns:
            List of recent memories
        """
        if not self.synced:
            return []

        # Filter by op_type if specified
        if op_type is not None:
            filtered = [m for m in self.memories if m['opType'] == op_type]
        else:
            filtered = self.memories

        # Sort by timestamp and return top N
        sorted_memories = sorted(filtered, key=lambda m: m['timestamp'], reverse=True)
        return sorted_memories[:limit]

    def get_by_user(
        self,
        user_address: str,
        limit: int = 50
    ) -> List[Dict]:
        """
        Get all memories for a specific user

        Args:
            user_address: Ethereum address
            limit: Maximum results

        Returns:
            List of user's memories
        """
        if not self.synced:
            return []

        user_lower = user_address.lower()

        if user_lower not in self.user_index:
            return []

        memory_ids = self.user_index[user_lower][:limit]
        results = [self.memories[i] for i in memory_ids]

        # Sort by timestamp (most recent first)
        results.sort(key=lambda m: m['timestamp'], reverse=True)

        return results

    def get_tag_stats(self) -> Dict[str, int]:
        """
        Get statistics about tag usage

        Returns:
            Dictionary of tag -> count
        """
        if not self.synced:
            return {}

        return {tag: len(ids) for tag, ids in self.tag_index.items()}

    def get_trending_tags(self, limit: int = 10) -> List[tuple]:
        """
        Get most popular tags

        Args:
            limit: Number of tags to return

        Returns:
            List of (tag, count) tuples
        """
        stats = self.get_tag_stats()
        sorted_tags = sorted(stats.items(), key=lambda x: x[1], reverse=True)
        return sorted_tags[:limit]

    def get_stats(self) -> Dict:
        """
        Get cache statistics

        Returns:
            Statistics dictionary
        """
        if not self.synced:
            return {
                "synced": False,
                "total_memories": 0,
                "unique_tags": 0,
                "unique_users": 0
            }

        insert_count = sum(1 for m in self.memories if m['opType'] == 0)
        search_count = sum(1 for m in self.memories if m['opType'] == 1)

        return {
            "synced": True,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "total_memories": len(self.memories),
            "insert_operations": insert_count,
            "search_operations": search_count,
            "unique_tags": len(self.tag_index),
            "unique_users": len(self.user_index),
            "most_active_user": max(self.user_index.items(), key=lambda x: len(x[1]))[0]
                if self.user_index else None
        }

    async def refresh(self):
        """Refresh cache from blockchain"""
        await self.sync_from_blockchain()


# Quick test
if __name__ == "__main__":
    print("MonadCache class loaded")
    print("Use: cache = MonadCache(monad_logger)")
    print("Then: await cache.sync_from_blockchain()")
