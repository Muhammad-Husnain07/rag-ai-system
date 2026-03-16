from typing import Optional


def sanitize_input(text: Optional[str]) -> str:
    """Sanitize user input: trim, collapse whitespace, and remove control chars."""
    if text is None:
        return ""
    # Basic cleaning: replace newlines with spaces, collapse whitespace
    cleaned = text.replace("\n", " ").replace("\r", " ")
    cleaned = " ".join(cleaned.split())
    # Remove non-printable characters
    cleaned = ''.join(ch for ch in cleaned if ch.isprintable())
    return cleaned
