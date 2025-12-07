# Simple local vector search without database
import json
import numpy as np
from typing import List, Dict, Any
import os
from embedding.embedder import generate_embedding, compute_similarity


class LocalVectorStore:
    """
    Simple file-based vector storage - no database needed
    Stores embeddings as JSON files
    """
    
    def __init__(self, storage_dir="data/embeddings"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        self.index_file = os.path.join(storage_dir, "index.json")
        self.load_index()
    
    def load_index(self):
        """Load the index from file"""
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r') as f:
                self.index = json.load(f)
        else:
            self.index = {
                "chunks": [],
                "embeddings": [],
                "metadata": []
            }
    
    def save_index(self):
        """Save the index to file"""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f)
    
    def add_chunk(self, text: str, embedding: List[float], metadata: Dict[str, Any] = None):
        """
        Add a chunk with its embedding
        
        Args:
            text: The text chunk
            embedding: 768-dim embedding vector
            metadata: Optional metadata (filename, chunk_id, etc.)
        """
        self.index["chunks"].append(text)
        self.index["embeddings"].append(embedding)
        self.index["metadata"].append(metadata or {})
        self.save_index()
    
    def search_similar(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar chunks
        
        Args:
            query: Search query text
            top_k: Number of results to return
            
        Returns:
            List of similar chunks with scores
        """
        if not self.index["chunks"]:
            return []
        
        # Generate embedding for query
        query_embedding = generate_embedding(query)
        
        # Calculate similarities
        similarities = []
        for i, stored_embedding in enumerate(self.index["embeddings"]):
            similarity = compute_similarity(query_embedding, stored_embedding)
            similarities.append({
                "chunk": self.index["chunks"][i],
                "metadata": self.index["metadata"][i],
                "score": similarity
            })
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x["score"], reverse=True)
        return similarities[:top_k]
    
    def clear(self):
        """Clear all stored data"""
        self.index = {
            "chunks": [],
            "embeddings": [],
            "metadata": []
        }
        self.save_index()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about stored data"""
        return {
            "total_chunks": len(self.index["chunks"]),
            "storage_size_mb": os.path.getsize(self.index_file) / (1024 * 1024) if os.path.exists(self.index_file) else 0
        }


# Example usage
if __name__ == "__main__":
    store = LocalVectorStore()
    
    # Add some chunks
    store.add_chunk(
        text="The current system handles 10,000 transactions per day.",
        embedding=generate_embedding("The current system handles 10,000 transactions per day."),
        metadata={"filename": "rfp1.txt", "chunk_id": 1}
    )
    
    store.add_chunk(
        text="Budget constraint is $500,000 for the entire project.",
        embedding=generate_embedding("Budget constraint is $500,000 for the entire project."),
        metadata={"filename": "rfp1.txt", "chunk_id": 2}
    )
    
    # Search
    results = store.search_similar("What is the budget?", top_k=2)
    
    print("Search Results:")
    for i, result in enumerate(results):
        print(f"\n{i+1}. Score: {result['score']:.3f}")
        print(f"   Text: {result['chunk']}")
        print(f"   Metadata: {result['metadata']}")
    
    print(f"\nStats: {store.get_stats()}")
