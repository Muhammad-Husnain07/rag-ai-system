from urllib.parse import urlparse
from typing import Tuple


def is_safe_url(url: str, allowed_schemes: Tuple[str, ...] = ("http", "https")) -> bool:
    """Return True if the URL uses an allowed scheme and has a host.

    - url can be None or empty; returns False in that case
    - Checks scheme is in allowed_schemes and domain (netloc) exists
    """
    if not url:
        return False
    try:
        parsed = urlparse(url)
        if parsed.scheme not in allowed_schemes:
            return False
        if not parsed.netloc:
            return False
        return True
    except Exception:
        return False
