import json
"""JSON utility helpers."""
from typing import Any, Optional


def to_json(obj: Any, indent: int = 2, ensure_ascii: bool = False) -> str:
    """Serialize a Python object to a JSON string.

    Falls back to string representation if object is not JSON-serializable.
    """
    try:
        return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii)
    except (TypeError, ValueError):
        return json.dumps(str(obj), indent=indent, ensure_ascii=ensure_ascii)


def parse_json(json_str: str, default: Any = None) -> Optional[Any]:
    """Parse a JSON string safely, returning default on error."""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default
