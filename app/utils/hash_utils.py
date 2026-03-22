import hashlib


def sha256_hexdigest(text: str) -> str:
    """Return the SHA-256 hex digest for the given text."""
    if text is None:
        text = ""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def md5_hexdigest(text: str) -> str:
    """Return the MD5 hex digest for the given text."""
    if text is None:
        text = ""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def sha1_hexdigest(text: str) -> str:
    """Return the SHA-1 hex digest for the given text."""
    if text is None:
        text = ""
    return hashlib.sha1(text.encode("utf-8")).hexdigest()
