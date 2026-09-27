from typing import TypedDict


class AgentState(TypedDict):
    query: str
    refined_query: str
    is_scripture_question: bool
    retrieved_verses: list[dict]
    answer: str
    validated: bool
    validation_notes: str
    retry_count: int