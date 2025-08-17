import faiss
import numpy as np
from utils.embedding_utils import embed_text

class Indexer:
    def __init__(self, embedding_dim=384):
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.documents = []

    def add_documents(self, docs: list[str]):
        embeddings = np.array([embed_text(doc) for doc in docs], dtype='float32')
        self.index.add(embeddings)
        self.documents.extend(docs)

    def search(self, query: str, top_k=5):
        query_embedding = np.array([embed_text(query)], dtype='float32')
        distances, indices = self.index.search(query_embedding, top_k)
        results = [self.documents[i] for i in indices[0]]
        return results, distances[0]