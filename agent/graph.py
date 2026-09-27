"""
Wires the nodes together into an actual LangGraph graph.

classify_query -> (casual_response -> END)
               -> query_refiner -> retriever -> synthesizer -> citation_validator
                                                                    -> (retry: increment_retry -> synthesizer)
                                                                    -> (end: END)
"""

from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes.classify_query import classify_query_node
from agent.nodes.casual_response import casual_response_node
from agent.nodes.query_refiner import query_refiner_node
from agent.nodes.retriever import retriever_node
from agent.nodes.synthesizer import synthesizer_node
from agent.nodes.citation_validator import citation_validator_node

MAX_RETRIES = 2


def route_after_classify(state: AgentState) -> str:
    return "retrieve" if state["is_scripture_question"] else "casual"


def route_after_validation(state: AgentState) -> str:
    if state["validated"]:
        return "end"
    if state.get("retry_count", 0) >= MAX_RETRIES:
        return "end"
    return "retry"


def increment_retry(state: AgentState) -> AgentState:
    state["retry_count"] = state.get("retry_count", 0) + 1
    return state


graph_builder = StateGraph(AgentState)

graph_builder.add_node("classify_query", classify_query_node)
graph_builder.add_node("casual_response", casual_response_node)
graph_builder.add_node("query_refiner", query_refiner_node)
graph_builder.add_node("retriever", retriever_node)
graph_builder.add_node("synthesizer", synthesizer_node)
graph_builder.add_node("citation_validator", citation_validator_node)
graph_builder.add_node("increment_retry", increment_retry)

graph_builder.set_entry_point("classify_query")

graph_builder.add_conditional_edges(
    "classify_query",
    route_after_classify,
    {"retrieve": "query_refiner", "casual": "casual_response"}
)

graph_builder.add_edge("casual_response", END)
graph_builder.add_edge("query_refiner", "retriever")
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
        "query": "what does the gita say about detachment from results",
        "refined_query": "",
        "is_scripture_question": True,
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