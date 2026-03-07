import pytest
from app.utils.text_chunker import chunk_text


def test_chunk_text_basic():
    """Test basic text chunking."""
    text = "This is a test document. " * 100
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    
    assert len(chunks) > 0
    assert all(isinstance(c, str) for c in chunks)


def test_chunk_text_empty():
    """Test chunking empty text."""
    chunks = chunk_text("")
    assert chunks == []


def test_chunk_text_with_overlap():
    """Test chunking with overlap."""
    text = "ABCDEFGHIJ" * 50
    chunks = chunk_text(text, chunk_size=20, overlap=5)
    
    assert len(chunks) > 1


def test_chunk_text_preserves_content():
    """Test that chunks preserve content."""
    text = "Hello world. This is a test."
    chunks = chunk_text(text, chunk_size=100, overlap=0)
    
    combined = " ".join(chunks)
    assert "Hello" in combined
    assert "world" in combined
