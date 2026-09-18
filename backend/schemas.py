"""
Defines the exact shape of what goes INTO the /chat endpoint (the request)
and what comes OUT of it (the response). FastAPI uses these to validate
incoming requests automatically and to document the API.
"""

from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str
    validated: bool
    validation_notes: str
    retrieved_verses: list[dict]
    retry_count: int