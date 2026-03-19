def identity(x):
    return x


def is_empty(value) -> bool:
    """Check if a value is empty (None, empty string, empty list, etc.)."""
    if value is None:
        return True
    if isinstance(value, (str, list, dict, set, tuple)):
        return len(value) == 0
    return False
