"""
Wires the nodes together into an actual LangGraph graph.
Retriever -> Synthesizer -> END (for now; Citation Validator comes next)
"""

from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes.retriever import retriever_node
from agent.nodes.synthesizer import synthesizer_node

graph_builder = StateGraph(AgentState)
graph_builder.add_node("retriever", retriever_node)
graph_builder.add_node("synthesizer", synthesizer_node)

graph_builder.set_entry_point("retriever")
graph_builder.add_edge("retriever", "synthesizer")
graph_builder.add_edge("synthesizer", END)

graph = graph_builder.compile()


if __name__ == "__main__":
    result = graph.invoke({
        "query": "what does the Gita say about detachment from results",
        "retrieved_verses": [],
        "answer": "",
    })
    print("\n--- ANSWER ---\n")
    print(result["answer"])