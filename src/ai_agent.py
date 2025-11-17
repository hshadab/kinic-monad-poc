"""
AI Agent powered by Claude (Anthropic)
Integrates with Kinic memory for context-aware responses
"""
import os
from typing import List, Dict, Optional
from anthropic import Anthropic


class AIAgent:
    """
    AI Memory Agent using Claude with Kinic memory integration
    """

    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307"):
        """
        Initialize AI agent with Anthropic

        Args:
            api_key: Anthropic API key
            model: Claude model to use (haiku for speed/cost, sonnet for quality)
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model

        # System prompt for the agent
        self.system_prompt = """You are a helpful AI memory agent built on Monad blockchain with Kinic storage.

Your capabilities:
- You can store and retrieve information using semantic search
- All your interactions are logged on Monad blockchain for transparency
- You help users remember, organize, and retrieve information

When users ask questions:
1. Search your memory for relevant context
2. Provide accurate, helpful answers based on stored information
3. If you don't have relevant information, say so clearly
4. Suggest storing new information when appropriate

Be concise, helpful, and transparent about your capabilities."""

    async def chat(
        self,
        message: str,
        memory_context: List[Dict] = None,
        conversation_history: List[Dict] = None
    ) -> str:
        """
        Generate AI response with memory context

        Args:
            message: User's message
            memory_context: Relevant memories from Kinic search
            conversation_history: Previous conversation turns

        Returns:
            AI-generated response
        """
        # Build context from memories
        context_text = self._build_context(memory_context)

        # Build messages array
        messages = []

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)

        # Add current message with context
        user_message = message
        if context_text:
            user_message = f"""Context from memory:
{context_text}

User question: {message}"""

        messages.append({
            "role": "user",
            "content": user_message
        })

        # Call Claude
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=self.system_prompt,
            messages=messages
        )

        return response.content[0].text

    def _build_context(self, memory_context: Optional[List[Dict]]) -> str:
        """
        Build context string from memory search results

        Args:
            memory_context: List of memory search results

        Returns:
            Formatted context string
        """
        if not memory_context:
            return ""

        context_parts = []
        for idx, result in enumerate(memory_context[:5], 1):  # Top 5 results
            text = result.get("text", "")
            score = result.get("score", 0)
            tag = result.get("tag", "")

            context_parts.append(
                f"[Memory {idx}] (relevance: {score:.2f}, tags: {tag})\n{text}"
            )

        return "\n\n".join(context_parts)

    async def chat_with_memory_search(
        self,
        message: str,
        search_function,
        top_k: int = 5,
        conversation_history: List[Dict] = None
    ) -> tuple[str, List[Dict]]:
        """
        Chat with automatic memory search

        Args:
            message: User's message
            search_function: Async function to search memories
            top_k: Number of memories to retrieve
            conversation_history: Previous conversation

        Returns:
            Tuple of (response, memories_used)
        """
        # Search for relevant memories
        memories = await search_function(message, top_k)

        # Generate response with context
        response = await self.chat(
            message=message,
            memory_context=memories,
            conversation_history=conversation_history
        )

        return response, memories


# Example usage
if __name__ == "__main__":
    import asyncio

    async def test():
        # Mock search function
        async def mock_search(query: str, top_k: int):
            return [
                {
                    "text": "ZKML enables verifiable ML inference using zero-knowledge proofs.",
                    "score": 0.89,
                    "tag": "zkml,test"
                }
            ]

        # Initialize agent
        agent = AIAgent(api_key=os.getenv("ANTHROPIC_API_KEY"))

        # Test chat
        response, memories = await agent.chat_with_memory_search(
            message="What is ZKML?",
            search_function=mock_search
        )

        print(f"Agent: {response}")
        print(f"Memories used: {len(memories)}")

    asyncio.run(test())
