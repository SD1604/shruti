"""
The Synthesizer Node — takes the verses the Retriever found and asks the
LLM to write a clear answer grounded in them, with citations.
"""

from agent.state import AgentState
from agent.llm_client import generate_answer


def build_prompt(query: str, verses: list[dict]) -> str:
    verses_text = "\n\n".join(
        f"[Chapter {v['chapter']}, Verse {v['verse_number']}]\n{v['text']}"
        for v in verses
    )
    return f"""You are answering a question about the Bhagavad Gita using ONLY the verses provided below. Do not add outside knowledge or claims not supported by these verses.

VERSES:
{verses_text}

QUESTION: {query}

Write a clear, well-explained answer based only on the verses above. When you reference a verse, cite it by chapter and verse number, like (2.47)."""


def synthesizer_node(state: AgentState) -> AgentState:
    prompt = build_prompt(state["query"], state["retrieved_verses"])
    answer = generate_answer(prompt)
    state["answer"] = answer
    return state