"""
Embeds verse text using Gemini's embedding API and loads it into a
persistent Chroma vector store.

Run this after fetch_gita.py and fetch_translation.py have both completed.
"""

import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import chromadb
from schemas.verse import Verse
from parse_gita import parse
from validate import validate_all
from agent.search_core import embed_text

VECTOR_STORE_PATH = "./vector_store"
COLLECTION_NAME = "scriptures"


def load_verses(verses: list[Verse]):
    client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
    collection = client.get_or_create_collection(COLLECTION_NAME)

    for i, v in enumerate(verses):
        text = v.english_translation or v.iast_transliteration
        embedding = embed_text(text, task_type="RETRIEVAL_DOCUMENT")

        collection.upsert(
            ids=[f"{v.text_name}_{v.chapter}_{v.verse_number}"],
            embeddings=[embedding],
            documents=[text],
            metadatas=[v.model_dump(exclude_none=True)],
        )

        if (i + 1) % 25 == 0:
            print(f"Embedded {i + 1}/{len(verses)} verses")

        time.sleep(0.1)  # stay comfortably within free-tier rate limits

    print(f"Done. {collection.count()} verses now in vector store.")


if __name__ == "__main__":
    verses = parse()
    valid, failed = validate_all(verses)
    load_verses(valid)