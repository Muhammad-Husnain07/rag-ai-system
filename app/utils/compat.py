def ensure_str(value) -> str:
    """Return string representation of value, converting None to empty string."""
    if value is None:
        return ""
    return str(value)
