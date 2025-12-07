# Embedding generation module
from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np

# Initialize the embedding model (all-mpnet-base-v2 produces 768-dimensional embeddings)
model = SentenceTransformer('all-mpnet-base-v2')


def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding vector for a single text string
    
    Args:
        text: Input text to embed
        
    Returns:
        List[float]: 768-dimensional embedding vector
    """
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()


def embed(text: str) -> List[float]:
    """
    Alias for generate_embedding for backward compatibility
    
    Args:
        text: Input text to embed
        
    Returns:
        List[float]: 768-dimensional embedding vector
    """
    return generate_embedding(text)


def embed_batch(texts: List[str], batch_size: int = 32) -> List[List[float]]:
    """
    Generate embeddings for multiple texts efficiently
    
    Args:
        texts: List of text strings to embed
        batch_size: Number of texts to process at once
        
    Returns:
        List of embedding vectors
    """
    embeddings = model.encode(texts, batch_size=batch_size, convert_to_numpy=True)
    return [emb.tolist() for emb in embeddings]


def compute_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Compute cosine similarity between two embeddings
    
    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector
        
    Returns:
        float: Cosine similarity score between -1 and 1
    """
    emb1 = np.array(embedding1)
    emb2 = np.array(embedding2)
    
    # Cosine similarity
    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    return float(similarity)


def get_model_info() -> dict:
    """
    Get information about the embedding model
    
    Returns:
        dict: Model name and dimensions
    """
    return {
        "model_name": "all-mpnet-base-v2",
        "dimensions": 768,
        "max_sequence_length": 384
    }
