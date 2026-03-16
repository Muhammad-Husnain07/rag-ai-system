from typing import Optional


def clamp(value: Optional[float], min_val: float, max_val: float) -> Optional[float]:
    """Clamp a numeric value to the [min_val, max_val] range.
    If value is None, returns None.
    """
    if value is None:
        return None
    if value < min_val:
        return min_val
    if value > max_val:
        return max_val
    return value
