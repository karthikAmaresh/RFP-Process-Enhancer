"""
RFP Document Processor
Combines text extraction, chunking, embedding, and storage
"""
from document_processing.embedding import generate_embedding
from document_processing.chunking import chunk_text
from memory.short_term import store_chunk as store_chunk_mongo
from document_processing.indexer import index_chunk
from typing import Dict, Any, Optional
import config


def process_rfp(rfp_text: str, filename: Optional[str] = None, storage: str = "both") -> Dict[str, Any]:
    """
    Process RFP text: chunk, embed, and store
    
    Args:
        rfp_text: The RFP document text
        filename: Optional filename for metadata
        storage: Where to store - "mongo", "search", or "both" (default)
        
    Returns:
        dict: Processing statistics
    """
    # Step 1: Chunk the text
    chunks = chunk_text(rfp_text)
    
    # Step 2: Process each chunk
    stored_count = 0
    for i, chunk in enumerate(chunks):
        # Generate embedding
        vec = generate_embedding(chunk)
        
        # Store in MongoDB
        if storage in ["mongo", "both"]:
            metadata = {"filename": filename, "chunk_id": i} if filename else {"chunk_id": i}
            store_chunk_mongo(chunk, vec, metadata)
        
        # Store in Azure Search
        if storage in ["search", "both"] and filename:
            index_chunk(chunk, vec, filename, i)
        
        stored_count += 1
    
    print(f"RFP loaded and {stored_count} embeddings stored.")
    
    return {
        "status": "success",
        "chunks_processed": stored_count,
        "total_chunks": len(chunks),
        "storage": storage,
        "filename": filename
    }


def process_rfp_from_file(file_path: str, storage: str = "both") -> Dict[str, Any]:
    """
    Process RFP from a text file
    
    Args:
        file_path: Path to the text file
        storage: Where to store - "mongo", "search", or "both"
        
    Returns:
        dict: Processing statistics
    """
    import os
    
    filename = os.path.basename(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        rfp_text = f.read()
    
    return process_rfp(rfp_text, filename=filename, storage=storage)


def process_rfp_from_blob(blob_name: str, storage: str = "both") -> Dict[str, Any]:
    """
    Process RFP from Azure Blob Storage
    
    Args:
        blob_name: Name of the blob file
        storage: Where to store - "mongo", "search", or "both"
        
    Returns:
        dict: Processing statistics
    """
    from document_processing.extract_text import extract_text_from_blob
    
    # Extract text from blob
    rfp_text = extract_text_from_blob(blob_name)
    
    return process_rfp(rfp_text, filename=blob_name, storage=storage)


def process_rfp_batch(rfp_texts: list, filenames: Optional[list] = None, storage: str = "both") -> Dict[str, Any]:
    """
    Process multiple RFP documents in batch
    
    Args:
        rfp_texts: List of RFP text documents
        filenames: Optional list of filenames (must match rfp_texts length)
        storage: Where to store - "mongo", "search", or "both"
        
    Returns:
        dict: Batch processing statistics
    """
    if filenames and len(filenames) != len(rfp_texts):
        raise ValueError("filenames length must match rfp_texts length")
    
    results = []
    total_chunks = 0
    
    for i, rfp_text in enumerate(rfp_texts):
        filename = filenames[i] if filenames else f"document_{i}"
        result = process_rfp(rfp_text, filename=filename, storage=storage)
        results.append(result)
        total_chunks += result["chunks_processed"]
    
    return {
        "status": "success",
        "documents_processed": len(rfp_texts),
        "total_chunks": total_chunks,
        "storage": storage,
        "results": results
    }


if __name__ == "__main__":
    # Example usage
    sample_text = """
    This is a sample RFP document for testing purposes.
    It contains multiple sentences and paragraphs.
    The system should extract, chunk, embed, and store this content.
    """
    
    result = process_rfp(sample_text, filename="sample.txt", storage="both")
    print(result)
