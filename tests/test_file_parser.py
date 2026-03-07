import pytest
from app.utils.file_parser import validate_file


def test_validate_file_allowed_extension():
    """Test validation with allowed extensions."""
    is_valid, error = validate_file("test.pdf", 1000)
    assert is_valid is True
    assert error is None


def test_validate_file_txt():
    """Test validation with TXT file."""
    is_valid, error = validate_file("document.txt", 1000)
    assert is_valid is True


def test_validate_file_markdown():
    """Test validation with MD file."""
    is_valid, error = validate_file("readme.md", 1000)
    assert is_valid is True


def test_validate_file_disallowed_extension():
    """Test validation with disallowed extension."""
    is_valid, error = validate_file("malicious.exe", 1000)
    assert is_valid is False
    assert "not allowed" in error.lower()


def test_validate_file_too_large():
    """Test validation with file too large."""
    max_size_mb = 10
    max_bytes = max_size_mb * 1024 * 1024
    is_valid, error = validate_file("large.pdf", max_bytes + 1, max_size_mb)
    assert is_valid is False
    assert "size" in error.lower()
