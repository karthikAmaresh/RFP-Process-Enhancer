"""
Search and Query Module for RFP Documents
Provides semantic search capabilities using embeddings
"""
from document_processing.embedding import generate_embedding
from memory.short_term import search_similar
from typing import List, Dict, Any, Optional


def query_rfp(question: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Query RFP documents using natural language question
    
    Args:
        question: Natural language question
        top_k: Number of top results to return
        
    Returns:
        List[Dict]: Matching chunks with text and metadata
    """
    # Generate embedding for the question
    query_embedding = generate_embedding(question)
    
    # Search for similar chunks
    results = search_similar(query_embedding, top_k=top_k)
    
    return results


def ask_rfp(question: str, top_k: int = 5, return_text_only: bool = False):
    """
    Ask a question about RFP documents and get answers
    
    Args:
        question: Natural language question
        top_k: Number of results to retrieve
        return_text_only: If True, return only text strings
        
    Returns:
        List: Either text strings or full result objects
    """
    results = query_rfp(question, top_k=top_k)
    
    if return_text_only:
        return [result.get('text', '') for result in results]
    
    return results


def search_by_keyword(keyword: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search RFP documents by keyword with semantic understanding
    
    Args:
        keyword: Search keyword or phrase
        top_k: Number of results
        
    Returns:
        List[Dict]: Matching results
    """
    return query_rfp(keyword, top_k=top_k)


def find_related_chunks(text: str, top_k: int = 5, exclude_self: bool = True) -> List[Dict[str, Any]]:
    """
    Find chunks related to a given text
    
    Args:
        text: Reference text
        top_k: Number of results
        exclude_self: Whether to exclude exact matches
        
    Returns:
        List[Dict]: Related chunks
    """
    query_embedding = generate_embedding(text)
    results = search_similar(query_embedding, top_k=top_k + 1 if exclude_self else top_k)
    
    if exclude_self:
        # Filter out the exact same text
        results = [r for r in results if r.get('text', '') != text][:top_k]
    
    return results


def get_context_for_agent(query: str, context_size: int = 3) -> str:
    """
    Get relevant context for agent analysis
    
    Args:
        query: The question or topic
        context_size: Number of chunks to retrieve
        
    Returns:
        str: Combined context text
    """
    results = query_rfp(query, top_k=context_size)
    
    context_parts = []
    for i, result in enumerate(results, 1):
        text = result.get('text', '')
        metadata = result.get('metadata', {})
        filename = metadata.get('filename', 'Unknown')
        
        context_parts.append(f"[Context {i} from {filename}]\n{text}\n")
    
    return "\n".join(context_parts)


# Example usage queries
EXAMPLE_QUERIES = {
    "business_process": "what is the business process?",
    "pain_points": "what are the pain points and problems?",
    "requirements": "what are the system requirements?",
    "budget": "what is the budget and cost information?",
    "users": "who are the users and stakeholders?",
    "timeline": "what is the timeline and schedule?",
    "technical": "what are the technical specifications?",
    "compliance": "what are the compliance requirements?"
}


def quick_query(query_type: str) -> List[Dict[str, Any]]:
    """
    Run a predefined query type
    
    Args:
        query_type: One of the EXAMPLE_QUERIES keys
        
    Returns:
        List[Dict]: Search results
    """
    question = EXAMPLE_QUERIES.get(query_type)
    if not question:
        raise ValueError(f"Unknown query type. Choose from: {list(EXAMPLE_QUERIES.keys())}")
    
    return query_rfp(question)


if __name__ == "__main__":
    # Example: Search for business process information
    results = query_rfp("what is the business process?")
    
    for i, result in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(f"Text: {result.get('text', '')[:200]}...")
        print(f"Metadata: {result.get('metadata', {})}")
