"""
Wrapper for kinic-cli binary to interact with Internet Computer
Runs the Rust CLI as a subprocess
"""
import subprocess
import json
import asyncio
import tempfile
import os
from typing import List, Dict
from pathlib import Path


class KinicRunner:
    """
    Runs kinic-cli as subprocess to interact with IC memory canister
    """

    def __init__(self, memory_id: str, identity: str, cli_path: str = None):
        """
        Initialize Kinic runner

        Args:
            memory_id: IC canister principal ID for memory storage
            identity: IC identity name to use
            cli_path: Path to kinic-cli binary (auto-detected if None)
        """
        self.memory_id = memory_id
        self.identity = identity

        # Auto-detect CLI path
        if cli_path is None:
            # Try common locations (Windows .exe first, then Unix)
            possible_paths = [
                "./kinic-cli/target/release/kinic-cli.exe",  # Windows
                "./kinic-cli/target/release/kinic-cli",      # Unix/WSL
                "/app/kinic-cli/target/release/kinic-cli.exe",
                "/app/kinic-cli/target/release/kinic-cli",
                "./kinic-cli.exe",
                "./kinic-cli",
                "kinic-cli.exe",
                "kinic-cli"
            ]
            for path in possible_paths:
                if Path(path).exists():
                    self.cli_path = path
                    break
            else:
                raise FileNotFoundError("kinic-cli binary not found. Please build it first.")
        else:
            self.cli_path = cli_path

        print(f" KinicRunner initialized with CLI at: {self.cli_path}")

    async def insert(self, content: str, tag: str = "general") -> Dict:
        """
        Insert content into Kinic memory via IC

        Args:
            content: Text content to store
            tag: Tag to associate with content

        Returns:
            Result dictionary from kinic-cli
        """
        # Write content to temp file (kinic-cli reads from files)
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_path = f.name

        try:
            # Build command - identity comes BEFORE subcommand
            cmd = [
                self.cli_path,
                "--identity", self.identity,
                "insert",
                "--memory-id", self.memory_id,
                "--file-path", temp_path,
                "--tag", tag
            ]

            # Run command
            output = await self._run_command(cmd)

            return {
                "status": "inserted",
                "output": output,
                "tag": tag
            }

        finally:
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass

    async def search(self, query: str, format: str = "json", top_k: int = 5) -> List[Dict]:
        """
        Search Kinic memory via IC

        Args:
            query: Search query string
            format: Output format (json, text, csv)
            top_k: Number of results (not directly supported by CLI, but included for API compatibility)

        Returns:
            List of search results
        """
        # Build command - identity comes BEFORE subcommand
        cmd = [
            self.cli_path,
            "--identity", self.identity,
            "search",
            "--memory-id", self.memory_id,
            "--query", query
        ]

        # Run command
        output = await self._run_command(cmd)

        # Parse output - kinic-cli returns text format
        try:
            # Try parsing as JSON first
            results = json.loads(output)
            return results if isinstance(results, list) else [{"text": output}]
        except json.JSONDecodeError:
            # Fallback to text parsing if JSON fails
            return [{"score": 1.0, "text": output}]

    async def list_memories(self) -> Dict:
        """
        List all deployed memory canisters

        Returns:
            List of memory canister IDs
        """
        cmd = [
            self.cli_path,
            "--identity", self.identity,
            "list"
        ]

        output = await self._run_command(cmd)

        return {
            "status": "success",
            "output": output
        }

    async def _run_command(self, cmd: List[str]) -> str:
        """
        Run subprocess command asynchronously

        Args:
            cmd: Command list to execute

        Returns:
            stdout output

        Raises:
            Exception: If command fails
        """
        # Log command (without full paths for cleanliness)
        cmd_str = " ".join([c if not c.startswith("/") else Path(c).name for c in cmd])
        print(f" Running: {cmd_str}")

        # Create subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Wait for completion
        stdout, stderr = await process.communicate()

        # Check for errors
        if process.returncode != 0:
            error_msg = stderr.decode().strip()
            print(f" kinic-cli error: {error_msg}")
            raise Exception(f"kinic-cli failed: {error_msg}")

        output = stdout.decode().strip()
        print(f" Command completed successfully")

        return output


# Quick test
if __name__ == "__main__":
    async def test():
        # Test with environment variables
        memory_id = os.getenv("KINIC_MEMORY_ID", "test-canister-id")
        identity = os.getenv("IC_IDENTITY_NAME", "default")

        runner = KinicRunner(memory_id, identity)

        # Test insert
        print("\n=== Testing Insert ===")
        result = await runner.insert("# Test\nThis is a test memory.", "test")
        print(json.dumps(result, indent=2))

        # Test search
        print("\n=== Testing Search ===")
        results = await runner.search("test memory")
        print(json.dumps(results, indent=2))

    asyncio.run(test())
