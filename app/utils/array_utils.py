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
