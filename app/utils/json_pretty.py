from typing import Any
import json


def pretty_json(obj: Any, indent: int = 2, sort_keys: bool = True) -> str:
    """Serialize a Python object to a human-friendly JSON string.

    - indent controls spacing
    - sort_keys sorts keys for readability
    - ensure_ascii is disabled to support non-ASCII chars
    """
    return json.dumps(obj, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
