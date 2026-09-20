"""
The actual search logic, extracted so it can be loaded ONCE and reused —
by both the MCP server (for standalone testing) and the FastAPI app
directly (for fast live serving, avoiding a subprocess restart per query).
"""

import chromadb
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
VECTOR_STORE_PATH = "./vector_store"
COLLECTION_NAME = "scriptures"

_embedder = None
_collection = None


def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBEDDING_MODEL)
    return _embedder


def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
        _collection = client.get_or_create_collection(COLLECTION_NAME)
    return _collection


def search_verses(query: str, top_k: int = 3) -> list[dict]:
    embedder = get_embedder()
    collection = get_collection()

    query_vector = embedder.encode([query]).tolist()
    results = collection.query(query_embeddings=query_vector, n_results=top_k)

    verses = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        verses.append({
            "text": doc,
            "chapter": meta.get("chapter"),
            "verse_number": meta.get("verse_number"),
            "translator": meta.get("translator"),
            "license": meta.get("license"),
            "source_url": meta.get("source_url"),
        })
    return verses