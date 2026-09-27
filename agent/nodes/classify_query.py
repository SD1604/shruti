from agent.state import AgentState
from agent.llm_client import generate_answer


def classify_query_node(state: AgentState) -> AgentState:
    prompt = f"""Classify the following message as either SCRIPTURE_QUESTION or CASUAL.

SCRIPTURE_QUESTION: a genuine question seeking teaching, meaning, or content from the Bhagavad Gita.
CASUAL: a greeting, small talk, or a message unrelated to the Gita's content.

Message: "{state['query']}"

Respond with exactly one word: SCRIPTURE_QUESTION or CASUAL"""

    response = generate_answer(prompt).strip().upper()
    state["is_scripture_question"] = "SCRIPTURE_QUESTION" in response
    return state