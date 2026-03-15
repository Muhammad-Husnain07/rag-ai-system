import re


def is_valid_email(email: str) -> bool:
    """Simple email validation using a regex."""
    if not isinstance(email, str):
        return False
    # Basic RFC-ish email validation; not exhaustive but good for quick checks
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None
