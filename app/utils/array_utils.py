def is_none(value) -> bool:
    return value is None


def sum_list(numbers: list) -> float:
    """Sum all numbers in a list."""
    return sum(numbers)


def uniq_list(items: list) -> list:
    """Return unique items from a list preserving order."""
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def chunk_list(items: list, chunk_size: int) -> list:
    """Split a list into chunks of specified size."""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def min_list(numbers: list) -> float:
    """Return minimum value in a list."""
    if not numbers:
        return 0
    return min(numbers)


def max_list(numbers: list) -> float:
    """Return maximum value in a list."""
    if not numbers:
        return 0
    return max(numbers)


def flatten_list(nested: list) -> list:
    """Flatten a nested list into a single level."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


def split_list(items: list, parts: int) -> list:
    """Split a list into approximately equal parts."""
    if parts <= 0:
        return []
    chunk_size = len(items) // parts
    remainder = len(items) % parts
    result = []
    idx = 0
    for i in range(parts):
        size = chunk_size + (1 if i < remainder else 0)
        result.append(items[idx:idx + size])
        idx += size
    return result


def find_duplicates(items: list) -> list:
    """Find duplicate items in a list."""
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)
