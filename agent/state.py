"""
Defines the "shape" of information that flows through the LangGraph agent
as it moves from node to node. Every node reads from this and writes back
into it.
"""

from typing import TypedDict

class AgentState(TypedDict):
    query: str
    retrieved_verses: list[dict]