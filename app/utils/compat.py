def ensure_str(value) -> str:
    return str(value) if value is not None else ""


def ensure_int(value, default: int = 0) -> int:
    """Ensure value is an integer, return default if not possible."""
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def ensure_bool(value) -> bool:
    """Convert value to boolean."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "on")
    return bool(value)
