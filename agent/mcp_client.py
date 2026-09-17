"""
A small helper that knows how to start the MCP server as a background
process and ask it a question via the real MCP protocol — the same way
the Inspector tool did when we tested Phase 2 manually.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PARAMS = StdioServerParameters(
    command="python",
    args=["mcp_server/server.py"],
)


async def call_search_verses(query: str, top_k: int = 3) -> list[dict]:
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "search_verses",
                arguments={"query": query, "top_k": top_k}
            )

            # The server might send back ONE block containing the whole
            # list, or MULTIPLE blocks (one per verse). Handle both.
            parsed_blocks = [json.loads(block.text) for block in result.content]

            if len(parsed_blocks) == 1 and isinstance(parsed_blocks[0], list):
                return parsed_blocks[0]   # one block held the full list
            return parsed_blocks           # each block was one verse


def search_verses_sync(query: str, top_k: int = 3) -> list[dict]:
    """LangGraph nodes are simplest to write as plain sync functions,
    so this wraps the async MCP call in a way a sync node can call."""
    return asyncio.run(call_search_verses(query, top_k))