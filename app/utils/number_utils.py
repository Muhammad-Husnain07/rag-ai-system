def is_numeric(value: str) -> bool:
    """Return True if value is numeric (int/float), otherwise False."""
    if value is None:
        return False
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def round_to(value: float, decimals: int = 2) -> float:
    """Round a float to the specified number of decimal places."""
    return round(value, decimals)


def is_positive(value: float) -> bool:
    """Return True if value is positive."""
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def is_negative(value: float) -> bool:
    """Return True if value is negative."""
    try:
        return float(value) < 0
    except (TypeError, ValueError):
        return False


def is_zero(value: float) -> bool:
    """Return True if value is zero."""
    try:
        return float(value) == 0
    except (TypeError, ValueError):
        return False


def in_range(value: float, min_val: float, max_val: float) -> bool:
    """Return True if value is within range [min_val, max_val]."""
    try:
        return min_val <= float(value) <= max_val
    except (TypeError, ValueError):
        return False
