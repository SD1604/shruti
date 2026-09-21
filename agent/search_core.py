"""
The actual search logic, extracted so it can be loaded ONCE and reused —
by both the MCP server (for standalone testing) and the FastAPI app
directly (for fast live serving).

Now uses Gemini's embedding API instead of a local model — this removes
our dependency on torch/sentence-transformers entirely, which is what
was causing our RAM problems for deployment.
"""

import os
import chromadb
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = "gemini-embedding-001"
VECTOR_STORE_PATH = "./vector_store"
COLLECTION_NAME = "scriptures"

_client = None
_collection = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client


def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
        _collection = client.get_or_create_collection(COLLECTION_NAME)
    return _collection


def embed_text(text: str, task_type: str) -> list[float]:
    """task_type must be 'RETRIEVAL_DOCUMENT' when embedding verses to
    store, or 'RETRIEVAL_QUERY' when embedding a user's question — using
    the right one improves search quality, since Gemini optimizes each
    differently even for the same underlying text."""
    client = get_client()
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(task_type=task_type),
    )
    return response.embeddings[0].values


def search_verses(query: str, top_k: int = 3) -> list[dict]:
    collection = get_collection()
    query_vector = embed_text(query, task_type="RETRIEVAL_QUERY")

    results = collection.query(query_embeddings=[query_vector], n_results=top_k)

    verses = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        verses.append({
            "text": doc,
            "sanskrit": meta.get("sanskrit_devanagari"),
            "chapter": meta.get("chapter"),
            "verse_number": meta.get("verse_number"),
            "translator": meta.get("translator"),
            "license": meta.get("license"),
            "source_url": meta.get("source_url"),
        })
    return verses