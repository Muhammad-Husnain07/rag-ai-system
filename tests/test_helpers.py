import pytest
from app.utils.helpers import (
    sanitize_filename,
    format_file_size,
    truncate_text,
    extract_keywords,
    validate_email,
    validate_password_strength
)


def test_sanitize_filename():
    """Test filename sanitization."""
    assert sanitize_filename("test file.pdf") == "test_file.pdf"
    assert sanitize_filename("test@file#name.pdf") == "testfilename.pdf"
    assert sanitize_filename("test   spaces   .pdf") == "test_spaces_.pdf"


def test_format_file_size():
    """Test file size formatting."""
    assert format_file_size(500) == "500.0 B"
    assert format_file_size(1024) == "1.0 KB"
    assert format_file_size(1024 * 1024) == "1.0 MB"
    assert format_file_size(1024 * 1024 * 1024) == "1.0 GB"


def test_truncate_text():
    """Test text truncation."""
    text = "This is a long text that needs to be truncated"
    assert truncate_text(text, 10) == "This is..."
    assert truncate_text(text, 50) == "This is a long text that needs to be truncated"
    assert truncate_text(text, 10, ">>") == "This i>>"


def test_extract_keywords():
    """Test keyword extraction."""
    text = "Python is a great programming language. Python is used for web development and data science."
    keywords = extract_keywords(text, 5)
    assert len(keywords) <= 5
    assert "python" in keywords
    assert "programming" in keywords or "language" in keywords


def test_validate_email():
    """Test email validation."""
    assert validate_email("test@example.com") is True
    assert validate_email("user.name@domain.co.uk") is True
    assert validate_email("invalid.email") is False
    assert validate_email("@domain.com") is False


def test_validate_password_strength():
    """Test password strength validation."""
    is_valid, msg = validate_password_strength("weak")
    assert is_valid is False
    
    is_valid, msg = validate_password_strength("Password1!")
    assert is_valid is True
    
    is_valid, msg = validate_password_strength("NoSpecial1")
    assert is_valid is False
    
    is_valid, msg = validate_password_strength("Nolower1!")
    assert is_valid is False
