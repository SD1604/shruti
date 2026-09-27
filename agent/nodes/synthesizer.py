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

Write your answer following these rules:
1. Use clear, everyday language — avoid academic or overly formal phrasing. If you use a Sanskrit term, briefly explain what it means the first time you use it.
2. Where a verse has a narrative setting (e.g. Krishna speaking to Arjuna on the battlefield), briefly mention that context.
3. After explaining what a verse says, briefly connect it to an ordinary, modern-day situation (work, relationships, stress, decision-making).
4. Cite verses by chapter and verse number, like (2.47).

Keep the answer focused and not overly long."""


def synthesizer_node(state: AgentState) -> AgentState:
    prompt = build_prompt(state["refined_query"], state["retrieved_verses"])
    answer = generate_answer(prompt)
    state["answer"] = answer
    return state