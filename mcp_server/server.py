"""
mcp_server/server.py

An MCP (Model Context Protocol) server that exposes our Gita vector store
as a callable tool: search_verses(query, top_k).

This is the "Front Desk" — it's the ONLY thing that talks to the vector
database directly. Everything else (the LangGraph agent, later) just asks
this server questions and gets clean answers back.
"""

from mcp.server.fastmcp import FastMCP
import chromadb
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
VECTOR_STORE_PATH = "./vector_store"
COLLECTION_NAME = "scriptures"

mcp = FastMCP("shruti-scripture-server")

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


@mcp.tool()
def search_verses(query: str, top_k: int = 3) -> list[dict]:
    """
    Search the scripture vector store for verses relevant to a query.

    Args:
        query: A natural language question or topic, e.g.
               "what does the Gita say about detachment from results"
        top_k: How many matching verses to return (default 3)

    Returns:
        A list of dicts, each containing the verse text and its metadata
        (chapter, verse number, translator, license, source URL).
    """

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



if __name__ == "__main__":
    mcp.run()