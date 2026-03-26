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
