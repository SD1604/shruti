"""
The FastAPI app — exposes your LangGraph pipeline as a real HTTP API.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import ChatRequest, ChatResponse
from agent.graph import graph
from agent.search_core import get_client, get_collection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once, when the server starts — connects to Gemini and the
    # vector store before any user can send a request.
    print("Connecting to Gemini and vector store...")
    get_client()
    get_collection()
    print("Ready to serve requests.")
    yield


app = FastAPI(title="Shruti API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://shruti-eta.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    result = graph.invoke({
        "query": request.query,
        "retrieved_verses": [],
        "answer": "",
        "validated": False,
        "validation_notes": "",
        "retry_count": 0,
    })

    return ChatResponse(
        answer=result["answer"],
        validated=result["validated"],
        validation_notes=result["validation_notes"],
        retrieved_verses=result["retrieved_verses"],
        retry_count=result["retry_count"],
    )