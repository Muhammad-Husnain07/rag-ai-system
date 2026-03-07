from typing import Optional
import os
import io


async def extract_text_from_file(file_content: bytes, file_extension: str) -> str:
    """
    Extract text from various file formats.
    
    Args:
        file_content: Raw file bytes
        file_extension: File extension (.pdf, .txt, .md)
    
    Returns:
        Extracted text content
    """
    if file_extension == ".pdf":
        return await extract_text_from_pdf(file_content)
    elif file_extension in [".txt", ".md"]:
        return extract_text_from_plain(file_content)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


async def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF using pdfplumber."""
    try:
        import pdfplumber
    except ImportError:
        raise ImportError("pdfplumber is required for PDF processing. Install with: pip install pdfplumber")
    
    text_parts = []
    
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    
    return "\n\n".join(text_parts)


def extract_text_from_plain(file_content: bytes) -> str:
    """Extract text from plain text or markdown files."""
    try:
        return file_content.decode("utf-8")
    except UnicodeDecodeError:
        return file_content.decode("latin-1", errors="ignore")


def validate_file(file_name: str, file_size: int, max_size_mb: int = 10) -> tuple[bool, Optional[str]]:
    """
    Validate uploaded file.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    allowed_extensions = [".pdf", ".txt", ".md"]
    
    _, ext = os.path.splitext(file_name)
    ext = ext.lower()
    
    if ext not in allowed_extensions:
        return False, f"File type not allowed. Supported types: {', '.join(allowed_extensions)}"
    
    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        return False, f"File size exceeds maximum of {max_size_mb}MB"
    
    return True, None
