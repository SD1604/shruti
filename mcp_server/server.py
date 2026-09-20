"""
mcp_server/server.py

An MCP server that exposes search_verses as a callable tool — useful for
standalone testing (via the Inspector) and for any other MCP-compatible
tool that wants to use this search. NOT used on the live serving path
for the web app anymore — see agent/nodes/retriever.py.
"""

from mcp.server.fastmcp import FastMCP
from agent.search_core import search_verses as _search_verses

mcp = FastMCP("shruti-scripture-server")


@mcp.tool()
def search_verses(query: str, top_k: int = 3) -> list[dict]:
    """Search the scripture vector store for verses relevant to a query."""
    return _search_verses(query, top_k)


if __name__ == "__main__":
    mcp.run()