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


def parse_bool(value) -> bool:
    """Parse string to boolean, returns None for invalid values."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lower = value.lower().strip()
        if lower in ("true", "1", "yes", "on"):
            return True
        if lower in ("false", "0", "no", "off", ""):
            return False
    return None


def ensure_float(value, default: float = 0.0) -> float:
    """Ensure value is a float, return default if not possible."""
    if isinstance(value, float):
        return value
    if isinstance(value, int):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def ensure_list(value, default=None) -> list:
    """Ensure value is a list, return default if not possible."""
    if isinstance(value, list):
        return value
    if value is None:
        return default if default is not None else []
    return [value]
