# Document embedding generation
from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np

# Initialize the embedding model
# all-mpnet-base-v2: 768 dimensions, better quality than all-MiniLM-L6-v2
model = SentenceTransformer("all-mpnet-base-v2")


def embed(text: str) -> List[float]:
    """
    Generate embedding vector for a single text
    
    Args:
        text: Text to embed
        
    Returns:
        List[float]: Embedding vector as a list
    """
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()  # store as list for DB


def generate_embedding(text: str) -> List[float]:
    """
    Alias for embed() function - generates embedding for text
    
    Args:
        text: Text to embed
        
    Returns:
        List[float]: Embedding vector as a list
    """
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()  # store as list for DB


def embed_batch(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts efficiently
    
    Args:
        texts: List of texts to embed
        
    Returns:
        List[List[float]]: List of embedding vectors
    """
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()


def embed_chunks(chunks: List[str], show_progress: bool = True) -> List[dict]:
    """
    Embed text chunks and return with metadata
    
    Args:
        chunks: List of text chunks to embed
        show_progress: Whether to show progress bar
        
    Returns:
        List[dict]: List of dictionaries containing chunk text and embedding
    """
    embeddings = model.encode(chunks, show_progress_bar=show_progress)
    
    result = []
    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        result.append({
            "id": idx,
            "text": chunk,
            "embedding": embedding.tolist(),
            "embedding_dim": len(embedding)
        })
    
    return result


def compute_similarity(text1: str, text2: str) -> float:
    """
    Compute cosine similarity between two texts
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        float: Similarity score between 0 and 1
    """
    emb1 = model.encode(text1)
    emb2 = model.encode(text2)
    
    # Compute cosine similarity
    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    
    return float(similarity)


def get_model_info() -> dict:
    """
    Get information about the embedding model
    
    Returns:
        dict: Model information including dimension and max sequence length
    """
    return {
        "model_name": "all-mpnet-base-v2",
        "embedding_dimension": model.get_sentence_embedding_dimension(),
        "max_seq_length": model.max_seq_length
    }
