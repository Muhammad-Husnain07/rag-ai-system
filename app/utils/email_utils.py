import re


def is_valid_email(email: str) -> bool:
    """Simple email validation using a regex."""
    if not isinstance(email, str):
        return False
    # Basic RFC-ish email validation; not exhaustive but good for quick checks
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None


def normalize_email(email: str) -> str:
    """Normalize an email by trimming and lowercasing."""
    if email is None:
        return email
    return email.strip().lower()


def extract_username(email: str) -> str | None:
    """Extract username (local part) from email address."""
    if '@' in email:
        return email.split('@')[0]
    return None
