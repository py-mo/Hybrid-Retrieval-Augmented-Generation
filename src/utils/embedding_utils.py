from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def embed_text(text: str) -> np.ndarray:
    """
    Embed the input text into a dense vector representation.
    """
    return model.encode(text)