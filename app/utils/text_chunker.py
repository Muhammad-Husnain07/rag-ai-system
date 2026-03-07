from typing import List
import re


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Input text to chunk
        chunk_size: Maximum size of each chunk
        overlap: Number of overlapping characters between chunks
    
    Returns:
        List of text chunks
    """
    if not text or not text.strip():
        return []
    
    text = re.sub(r'\s+', ' ', text).strip()
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        
        if end >= text_length:
            chunks.append(text[start:].strip())
            break
        
        chunk = text[start:end]
        
        sentence_end = max(
            chunk.rfind('.'),
            chunk.rfind('!'),
            chunk.rfind('?'),
            chunk.rfind('\n')
        )
        
        if sentence_end > chunk_size // 2:
            end = start + sentence_end + 1
        
        chunks.append(chunk.strip())
        start = end - overlap
    
    return [c for c in chunks if c]
