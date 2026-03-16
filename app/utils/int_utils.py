from typing import Optional


def safe_int_parse(value: Optional[str], default: int = 0) -> int:
    """Parse an integer from a string safely.

    - If value is None or invalid, return default.
    - Non-integer strings return the provided default.
    """
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
