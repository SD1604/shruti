import time
from agent.state import AgentState
from agent.search_core import search_verses


def retriever_node(state: AgentState) -> AgentState:
    start = time.time()
    verses = search_verses(state["query"], top_k=3)
    state["retrieved_verses"] = verses
    print(f"[TIMING] retriever_node took {time.time() - start:.2f}s")
    return state