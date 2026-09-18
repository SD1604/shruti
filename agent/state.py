"""
Defines the "shape" of information that flows through the LangGraph agent
as it moves from node to node. Every node reads from this and writes back
into it.
"""

from typing import TypedDict


class AgentState(TypedDict):
    query: str                    # the user's original question
    retrieved_verses: list[dict]  # filled in by the Retriever node
    answer: str                   # filled in by the Synthesizer node