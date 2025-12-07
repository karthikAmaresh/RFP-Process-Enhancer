# Short-term memory management for agents
from pymongo import MongoClient
from typing import List, Dict, Any, Optional
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Initialize MongoDB client
client = MongoClient(config.MONGO_CONN_STR) if hasattr(config, 'MONGO_CONN_STR') else None
db = client["rfp_db"] if client else None
collection = db["embeddings"] if db else None


def store_chunk(chunk_text: str, embedding: List[float], metadata: Optional[Dict[str, Any]] = None) -> str:
    """
    Store a text chunk with its embedding in MongoDB
    
    Args:
        chunk_text: The text content
        embedding: The embedding vector
        metadata: Optional metadata (filename, chunk_id, etc.)
        
    Returns:
        str: The inserted document ID
    """
    if not collection:
        raise Exception("MongoDB not configured. Set MONGO_CONN_STR in .env")
    
    doc = {
        "text": chunk_text,
        "vector": embedding,
        "metadata": metadata or {},
        "timestamp": datetime.utcnow()
    }
    
    result = collection.insert_one(doc)
    return str(result.inserted_id)


def store_chunks_batch(chunks_data: List[Dict[str, Any]]) -> List[str]:
    """
    Store multiple chunks in a batch operation
    
    Args:
        chunks_data: List of dicts with 'text', 'vector', and optional 'metadata'
        
    Returns:
        List[str]: List of inserted document IDs
    """
    if not collection:
        raise Exception("MongoDB not configured. Set MONGO_CONN_STR in .env")
    
    documents = []
    for chunk_data in chunks_data:
        doc = {
            "text": chunk_data.get("text", ""),
            "vector": chunk_data.get("vector", []),
            "metadata": chunk_data.get("metadata", {}),
            "timestamp": datetime.utcnow()
        }
        documents.append(doc)
    
    result = collection.insert_many(documents)
    return [str(id) for id in result.inserted_ids]


def search_similar(query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search for similar vectors using MongoDB vector search
    Note: Requires MongoDB Atlas with vector search index
    
    Args:
        query_vector: The query embedding vector
        top_k: Number of top results to return
        
    Returns:
        List[Dict]: Similar documents with text and metadata
    """
    if not collection:
        raise Exception("MongoDB not configured. Set MONGO_CONN_STR in .env")
    
    results = collection.aggregate([
        {
            "$search": {
                "vector": {
                    "path": "vector",
                    "query": query_vector,
                    "numCandidates": 100,
                    "limit": top_k
                }
            }
        }
    ])

    return list(results)


def search_similar_vectors(query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
    """
    Alias for search_similar() - kept for backward compatibility
    """
    return search_similar(query_vector, top_k=limit)


def get_chunks_by_filename(filename: str) -> List[Dict[str, Any]]:
    """
    Retrieve all chunks for a specific file
    
    Args:
        filename: The filename to search for
        
    Returns:
        List[Dict]: All chunks from that file
    """
    if not collection:
        raise Exception("MongoDB not configured. Set MONGO_CONN_STR in .env")
    
    results = collection.find({"metadata.filename": filename})
    return list(results)


def delete_chunks_by_filename(filename: str) -> int:
    """
    Delete all chunks associated with a filename
    
    Args:
        filename: The filename whose chunks should be deleted
        
    Returns:
        int: Number of documents deleted
    """
    if not collection:
        raise Exception("MongoDB not configured. Set MONGO_CONN_STR in .env")
    
    result = collection.delete_many({"metadata.filename": filename})
    return result.deleted_count


def clear_all_chunks() -> int:
    """
    Clear all stored chunks (use with caution!)
    
    Returns:
        int: Number of documents deleted
    """
    if not collection:
        raise Exception("MongoDB not configured. Set MONGO_CONN_STR in .env")
    
    result = collection.delete_many({})
    return result.deleted_count


class ShortTermMemory:
    """
    Short-term memory for agent conversations and context
    """
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.memory_collection = db["agent_memory"] if db else None
        self.context = []
    
    def add_message(self, role: str, content: str):
        """Add a message to memory"""
        self.context.append({"role": role, "content": content})
        
        if self.memory_collection:
            self.memory_collection.insert_one({
                "agent": self.agent_name,
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow()
            })
    
    def get_context(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get recent conversation context"""
        return self.context[-limit:]
    
    def clear(self):
        """Clear memory"""
        self.context = []
