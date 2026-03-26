def identity(x):
    return x


def is_empty(value) -> bool:
    """Check if a value is empty (None, empty string, empty list, etc.)."""
    if value is None:
        return True
    if isinstance(value, (str, list, dict, set, tuple)):
        return len(value) == 0
    return False


def flatten_list(nested_list: list) -> list:
    """Flatten a nested list into a single list."""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


def get_size(obj) -> int:
    """Get size of an object in bytes (like sys.getsizeof)."""
    import sys
    return sys.getsizeof(obj)
