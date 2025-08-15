from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    def __init__(self, model: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        """
        """
        self.model = SentenceTransformer(model)

    def embed_text(self, text: str, model) -> np.ndarray:
        """
        Embed the input text into a dense vector representation.
        """
        return self.model.encode(text)