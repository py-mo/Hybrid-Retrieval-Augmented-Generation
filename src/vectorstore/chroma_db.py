from chromadb import Client
from chromadb.config import Settings
import uuid
from utils import Embedder


class ChromaDB:
    def __init__(self, embedder: Embedder, persist_directory: str):
        self.client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_directory))
        self.collection = self.client.get_or_create_collection(name="documents")
        self.embedder = embedder

    def store_chunks(self, doc_id, chunks):
        """
        1. Embed each chunk
        2. Store in Chroma
        """
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc_id}_{i}_{uuid.uuid4().hex[:8]}"
            embedding = self.embedder.embed(chunk)
            self.collection.add(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"doc_id": doc_id, "chunk_index": i}]
            )
        return len(chunks)

    def search(self, query, embedder, top_k=5):
        """
        Search query against Chroma
        """
        query_embedding = embedder.embed(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results
