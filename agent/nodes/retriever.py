from agent.state import AgentState
from agent.search_core import search_verses


def retriever_node(state: AgentState) -> AgentState:
    verses = search_verses(state["refined_query"], top_k=3)
    state["retrieved_verses"] = verses
    return state