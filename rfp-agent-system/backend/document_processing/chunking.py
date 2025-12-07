# Document chunking for processing
from typing import List


def chunk_text(text: str, max_tokens: int = 200) -> List[str]:
    """
    Split text into chunks of specified word count
    
    Args:
        text: The text to chunk
        max_tokens: Maximum number of words per chunk (default: 200)
        
    Returns:
        List[str]: List of text chunks
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_tokens):
        chunk = " ".join(words[i:i+max_tokens])
        chunks.append(chunk)

    return chunks


def chunk_text_with_overlap(text: str, chunk_size: int = 700, overlap: int = 100) -> List[str]:
    """
    Split text into chunks with overlapping words for better context preservation
    
    Args:
        text: The text to chunk
        chunk_size: Number of words per chunk
        overlap: Number of overlapping words between chunks
        
    Returns:
        List[str]: List of overlapping text chunks
    """
    words = text.split()
    chunks = []
    
    if len(words) <= chunk_size:
        return [text]
    
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        
        # Move start position forward, accounting for overlap
        start += (chunk_size - overlap)
        
        # Break if we've processed all words
        if end >= len(words):
            break
    
    return chunks


def chunk_by_sentences(text: str, max_words: int = 700) -> List[str]:
    """
    Chunk text by sentences, keeping sentences together within word limit
    
    Args:
        text: The text to chunk
        max_words: Maximum words per chunk
        
    Returns:
        List[str]: List of sentence-based chunks
    """
    import re
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for sentence in sentences:
        sentence_word_count = len(sentence.split())
        
        if current_word_count + sentence_word_count <= max_words:
            current_chunk.append(sentence)
            current_word_count += sentence_word_count
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_word_count = sentence_word_count
    
    # Add the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks


def chunk_by_paragraphs(text: str, max_words: int = 700) -> List[str]:
    """
    Chunk text by paragraphs, keeping paragraphs together within word limit
    
    Args:
        text: The text to chunk
        max_words: Maximum words per chunk
        
    Returns:
        List[str]: List of paragraph-based chunks
    """
    # Split by double newlines (paragraphs)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for paragraph in paragraphs:
        paragraph_word_count = len(paragraph.split())
        
        if current_word_count + paragraph_word_count <= max_words:
            current_chunk.append(paragraph)
            current_word_count += paragraph_word_count
        else:
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
            
            # If single paragraph exceeds max_words, chunk it separately
            if paragraph_word_count > max_words:
                para_chunks = chunk_text(paragraph, max_words)
                chunks.extend(para_chunks)
                current_chunk = []
                current_word_count = 0
            else:
                current_chunk = [paragraph]
                current_word_count = paragraph_word_count
    
    # Add the last chunk
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
    
    return chunks
