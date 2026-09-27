"""
Takes the raw user query and rewrites it into a clearer, more specific
version — better for both vector search (removes vagueness/typos) and
for guiding the Synthesizer's eventual answer structure.
"""

from agent.state import AgentState
from agent.llm_client import generate_answer


def query_refiner_node(state: AgentState) -> AgentState:
    prompt = f"""Rewrite the following user question about the Bhagavad Gita into a 
clear, specific, well-formed question — correcting vagueness, typos, or informal 
phrasing, while preserving the original intent exactly. Do not answer it. 
Respond with ONLY the rewritten question, nothing else.

Original: "{state['query']}" """

    state["refined_query"] = generate_answer(prompt).strip()
    return state