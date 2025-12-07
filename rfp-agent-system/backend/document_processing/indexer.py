# Document indexing for retrieval
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
)
from azure.core.credentials import AzureKeyCredential
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Initialize Search Client (only if credentials are provided)
search_client = None
if config.SEARCH_ENDPOINT and config.SEARCH_API_KEY:
    try:
        search_client = SearchClient(
            endpoint=config.SEARCH_ENDPOINT,
            index_name=config.SEARCH_INDEX_NAME,
            credential=AzureKeyCredential(config.SEARCH_API_KEY)
        )
    except Exception as e:
        print(f"Warning: Could not initialize Azure Search client: {e}")


def index_chunk(chunk_text: str, embedding: List[float], file: str, chunk_id: int) -> None:
    """
    Index a single chunk with its embedding
    
    Args:
        chunk_text: The text content of the chunk
        embedding: The embedding vector
        file: The source filename
        chunk_id: The chunk identifier
    """
    if not search_client:
        print("Warning: Azure Search not configured. Skipping indexing.")
        return
        
    doc = {
        "id": f"{file}-{chunk_id}",
        "content": chunk_text,
        "embedding": embedding,
        "fileName": file,
        "chunk": chunk_id
    }
    search_client.upload_documents([doc])


def index_chunks_batch(chunks_data: List[Dict[str, Any]], file: str) -> Dict[str, Any]:
    """
    Index multiple chunks in a batch operation
    
    Args:
        chunks_data: List of dictionaries with 'text' and 'embedding' keys
        file: The source filename
        
    Returns:
        dict: Results of the indexing operation
    """
    if not search_client:
        print("Warning: Azure Search not configured. Skipping batch indexing.")
        return {"uploaded": 0, "succeeded": 0, "failed": len(chunks_data)}
        
    documents = []
    for idx, chunk_data in enumerate(chunks_data):
        doc = {
            "id": f"{file}-{idx}",
            "content": chunk_data.get("text", ""),
            "embedding": chunk_data.get("embedding", []),
            "fileName": file,
            "chunk": idx
        }
        documents.append(doc)
    
    result = search_client.upload_documents(documents)
    
    return {
        "uploaded": len(documents),
        "succeeded": sum(1 for r in result if r.succeeded),
        "failed": sum(1 for r in result if not r.succeeded)
    }


def search_similar_chunks(query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search for similar chunks using vector similarity
    
    Args:
        query_embedding: The query vector
        top_k: Number of top results to return
        
    Returns:
        List[Dict]: List of similar chunks with their content and metadata
    """
    if not search_client:
        print("Warning: Azure Search not configured. Returning empty results.")
        return []
        
    from azure.search.documents.models import VectorizedQuery
    
    vector_query = VectorizedQuery(
        vector=query_embedding,
        k_nearest_neighbors=top_k,
        fields="embedding"
    )
    
    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query],
        select=["id", "content", "fileName", "chunk"]
    )
    
    return [
        {
            "id": result["id"],
            "content": result["content"],
            "fileName": result["fileName"],
            "chunk": result["chunk"],
            "score": result.get("@search.score", 0)
        }
        for result in results
    ]


def search_with_text(query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search using text query (keyword search)
    
    Args:
        query_text: The search query
        top_k: Number of top results to return
        
    Returns:
        List[Dict]: List of matching chunks
    """
    if not search_client:
        print("Warning: Azure Search not configured. Returning empty results.")
        return []
        
    results = search_client.search(
        search_text=query_text,
        top=top_k,
        select=["id", "content", "fileName", "chunk"]
    )
    
    return [
        {
            "id": result["id"],
            "content": result["content"],
            "fileName": result["fileName"],
            "chunk": result["chunk"],
            "score": result.get("@search.score", 0)
        }
        for result in results
    ]


def hybrid_search(query_text: str, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Perform hybrid search combining text and vector search
    
    Args:
        query_text: The text query
        query_embedding: The query embedding vector
        top_k: Number of top results to return
        
    Returns:
        List[Dict]: List of matching chunks
    """
    if not search_client:
        print("Warning: Azure Search not configured. Returning empty results.")
        return []
        
    from azure.search.documents.models import VectorizedQuery
    
    vector_query = VectorizedQuery(
        vector=query_embedding,
        k_nearest_neighbors=top_k,
        fields="embedding"
    )
    
    results = search_client.search(
        search_text=query_text,
        vector_queries=[vector_query],
        top=top_k,
        select=["id", "content", "fileName", "chunk"]
    )
    
    return [
        {
            "id": result["id"],
            "content": result["content"],
            "fileName": result["fileName"],
            "chunk": result["chunk"],
            "score": result.get("@search.score", 0)
        }
        for result in results
    ]


def delete_document_chunks(filename: str) -> Dict[str, Any]:
    """
    Delete all chunks associated with a specific file
    
    Args:
        filename: The filename whose chunks should be deleted
        
    Returns:
        dict: Results of the deletion operation
    """
    if not search_client:
        print("Warning: Azure Search not configured. Cannot delete chunks.")
        return {"deleted": 0}
        
    # Search for all chunks from this file
    results = search_client.search(
        search_text="*",
        filter=f"fileName eq '{filename}'",
        select=["id"]
    )
    
    doc_ids = [{"id": result["id"]} for result in results]
    
    if doc_ids:
        delete_result = search_client.delete_documents(doc_ids)
        return {
            "deleted": len(doc_ids),
            "succeeded": sum(1 for r in delete_result if r.succeeded),
            "failed": sum(1 for r in delete_result if not r.succeeded)
        }
    
    return {"deleted": 0, "succeeded": 0, "failed": 0}


def create_search_index():
    """
    Create the search index with vector search configuration
    This should be run once to set up the index
    """
    if not config.SEARCH_ENDPOINT or not config.SEARCH_API_KEY:
        print("Warning: Azure Search credentials not configured. Cannot create index.")
        return None
        
    index_client = SearchIndexClient(
        endpoint=config.SEARCH_ENDPOINT,
        credential=AzureKeyCredential(config.SEARCH_API_KEY)
    )
    
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=768,  # all-mpnet-base-v2 dimension
            vector_search_profile_name="my-vector-config"
        ),
        SimpleField(name="fileName", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="chunk", type=SearchFieldDataType.Int32, filterable=True),
    ]
    
    vector_search = VectorSearch(
        profiles=[
            VectorSearchProfile(
                name="my-vector-config",
                algorithm_configuration_name="my-hnsw-config"
            )
        ],
        algorithms=[
            HnswAlgorithmConfiguration(name="my-hnsw-config")
        ]
    )
    
    index = SearchIndex(
        name=config.SEARCH_INDEX_NAME,
        fields=fields,
        vector_search=vector_search
    )
    
    index_client.create_or_update_index(index)
    return {"status": "Index created successfully"}
