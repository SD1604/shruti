"""
The Retriever Node — the first (and for now, only) step in our agent's
flow. Takes the current state, asks the MCP server for matching verses,
and writes the results back into the state.
"""

from agent.state import AgentState
from agent.mcp_client import search_verses_sync

def retriever_node(state: AgentState) -> AgentState:
    verses = search_verses_sync(state["query"], top_k=3)
    state["retrieved_verses"] = verses
    return state

