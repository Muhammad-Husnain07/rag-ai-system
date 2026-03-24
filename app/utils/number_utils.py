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
