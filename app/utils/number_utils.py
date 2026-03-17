def is_numeric(value: str) -> bool:
    """Return True if value is numeric (int/float), otherwise False."""
    if value is None:
        return False
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False
