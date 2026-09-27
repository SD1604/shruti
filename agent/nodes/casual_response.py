from agent.state import AgentState
from agent.llm_client import generate_answer


def casual_response_node(state: AgentState) -> AgentState:
    prompt = f"""You are Shruti, a friendly assistant focused on the Bhagavad Gita. 
Respond warmly and briefly to this casual message, and gently invite the user to ask 
a question about the Gita's teachings.

Message: "{state['query']}" """

    state["answer"] = generate_answer(prompt)
    state["validated"] = True
    state["validation_notes"] = "Casual message — no scripture claims made."
    state["retrieved_verses"] = []
    return state