"""
Wires the nodes together into an actual LangGraph graph. Right now there's
only one node (Retriever), so the graph is trivially simple — but this is
the same structure we'll extend in later phases.
"""

from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes.retriever import retriever_node

graph_builder = StateGraph(AgentState)
graph_builder.add_node("retriever_node", retriever_node)
graph_builder.set_entry_point("retriever_node")
graph_builder.add_edge("retriever_node", END)

graph = graph_builder.compile()



if __name__ == "__main__":
    result = graph.invoke({"query": "what does the Gita say about lust", "retrieved_verses": []})
    for v in result["retrieved_verses"]:
        print(f"\nChapter {v['chapter']}, Verse {v['verse_number']}:")
        print(v["text"])