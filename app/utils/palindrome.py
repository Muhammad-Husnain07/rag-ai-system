import re


def is_palindrome(s: str) -> bool:
    """Check if a string is palindrome ignoring non-alphanumeric and case."""
    if s is None:
        return False
    s_clean = re.sub(r'[^A-Za-z0-9]', '', s).lower()
    return s_clean == s_clean[::-1]
