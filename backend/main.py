"""
The FastAPI app — exposes your LangGraph pipeline as a real HTTP API.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import ChatRequest, ChatResponse
from agent.graph import graph
from agent.search_core import get_embedder, get_collection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once, when the server starts — loads the embedding model and
    # connects to the vector store BEFORE any user can send a request,
    # so nobody's first question has to eat that ~27s loading cost.
    print("Loading embedding model and vector store...")
    get_embedder()
    get_collection()
    print("Ready to serve requests.")
    yield
    # (nothing needed on shutdown)


app = FastAPI(title="Shruti API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UNVERIFIED_WARNING = (
    "⚠️ **This answer could not be fully verified against the source verses "
    "after multiple attempts. Please treat it with caution and check the "
    "cited verses yourself.**\n\n"
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

    answer = result["answer"]
    if not result["validated"]:
        answer = UNVERIFIED_WARNING + answer

    return ChatResponse(
        answer=answer,
        validated=result["validated"],
        validation_notes=result["validation_notes"],
        retrieved_verses=result["retrieved_verses"],
        retry_count=result["retry_count"],
    )