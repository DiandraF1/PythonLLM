# chromadb.py

import json
import chromadb
from sentence_transformers import SentenceTransformer

# Încarcă datele din fișierul JSON
def load_book_summaries(path="data/book_summaries.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Creează și returnează o colecție Chroma
def create_chroma_collection():
    # Inițializează modelul de embedding
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Încarcă rezumatele
    summaries = load_book_summaries()
    titles = list(summaries.keys())
    texts = list(summaries.values())

    # Creează embedding-uri
    embeddings = model.encode(texts).tolist()

    # Inițializează clientul Chroma
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="book_summaries")

    # Populează colecția
    collection.add(
        documents=texts,
        ids=titles,
        embeddings=embeddings,
        metadatas=[{"title": title} for title in titles]
    )

  
    return collection
