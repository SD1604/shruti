from typing import TypedDict


class AgentState(TypedDict):
    query: str
    retrieved_verses: list[dict]
    answer: str
    validated: bool
    validation_notes: str
    retry_count: int