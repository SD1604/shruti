"""
Wires the nodes together into an actual LangGraph graph.
Retriever -> Synthesizer -> Citation Validator -> (retry Synthesizer if failed, up to 2 times) -> END
"""

from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes.retriever import retriever_node
from agent.nodes.synthesizer import synthesizer_node
from agent.nodes.citation_validator import citation_validator_node

MAX_RETRIES = 2


def route_after_validation(state: AgentState) -> str:
    """Decides what happens after validation: if it passed, we're done.
    If it failed and we haven't retried too many times yet, go back to
    the Synthesizer to try writing a stricter, more careful answer."""
    if state["validated"]:
        return "end"
    if state.get("retry_count", 0) >= MAX_RETRIES:
        return "end"  # give up after MAX_RETRIES, return best-effort answer
    return "retry"


def increment_retry(state: AgentState) -> AgentState:
    state["retry_count"] = state.get("retry_count", 0) + 1
    return state


graph_builder = StateGraph(AgentState)
graph_builder.add_node("retriever", retriever_node)
graph_builder.add_node("synthesizer", synthesizer_node)
graph_builder.add_node("citation_validator", citation_validator_node)
graph_builder.add_node("increment_retry", increment_retry)

graph_builder.set_entry_point("retriever")
graph_builder.add_edge("retriever", "synthesizer")
graph_builder.add_edge("synthesizer", "citation_validator")

graph_builder.add_conditional_edges(
    "citation_validator",
    route_after_validation,
    {"end": END, "retry": "increment_retry"}
)
graph_builder.add_edge("increment_retry", "synthesizer")

graph = graph_builder.compile()


if __name__ == "__main__":
    result = graph.invoke({
        "query": "what does the Gita say about detachment from results",
        "retrieved_verses": [],
        "answer": "",
        "validated": False,
        "validation_notes": "",
        "retry_count": 0,
    })
    print("\n--- ANSWER ---\n")
    print(result["answer"])
    print("\n--- VALIDATION ---\n")
    print(f"Passed: {result['validated']}")
    print(f"Notes: {result['validation_notes']}")
    print(f"Retries used: {result['retry_count']}")