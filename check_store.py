import chromadb
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

client = chromadb.PersistentClient(path="./vector_store")
collection = client.get_or_create_collection("scriptures")
print(f"Total verses stored: {collection.count()}")

embedder = SentenceTransformer(EMBEDDING_MODEL)
query = "duty without attachment to results"
query_vec = embedder.encode([query]).tolist()

results = collection.query(query_embeddings=query_vec, n_results=3)
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"\nChapter {meta['chapter']}, Verse {meta['verse_number']}: {doc}")