import hashlib


def sha256_hexdigest(text: str) -> str:
    """Return the SHA-256 hex digest for the given text."""
    if text is None:
        text = ""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
