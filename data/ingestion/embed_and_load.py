"""
Embeds verse text locally and loads it into a persistent Chroma vector store.

NOTE ON MODEL CHOICE: Originally used Qwen/Qwen3-Embedding-0.6B, but that
requires transformers>=4.51.0, which in turn requires torch>=2.5. PyTorch
dropped support for Intel Macs (x86_64) after version 2.2.2, so Qwen3 cannot
run on this machine. Switched to a well-established multilingual model that
works fine with the older, Intel-Mac-compatible transformers/torch versions.

Run this after fetch_gita.py and fetch_translation.py have both completed.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from sentence_transformers import SentenceTransformer
import chromadb
from schemas.verse import Verse
from parse_gita import parse
from validate import validate_all

VECTOR_STORE_PATH = "./vector_store"
COLLECTION_NAME = "scriptures"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"


def load_verses(verses: list[Verse], batch_size: int = 32):
    embedder = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
    collection = client.get_or_create_collection(COLLECTION_NAME)

    for i in range(0, len(verses), batch_size):
        batch = verses[i:i + batch_size]
        texts = [v.english_translation or v.iast_transliteration for v in batch]
        embeddings = embedder.encode(texts).tolist()

        collection.upsert(
            ids=[f"{v.text_name}_{v.chapter}_{v.verse_number}" for v in batch],
            embeddings=embeddings,
            documents=texts,
            metadatas=[v.model_dump(exclude_none=True) for v in batch],
        )
        print(f"Loaded batch {i // batch_size + 1}")

    print(f"Done. {collection.count()} verses now in vector store.")


if __name__ == "__main__":
    verses = parse()
    valid, failed = validate_all(verses)
    load_verses(valid)