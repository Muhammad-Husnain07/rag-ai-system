from datetime import datetime


def format_datetime(dt: datetime | None) -> str:
    """Return ISO8601 UTC string for a datetime, or empty string if None."""
    if dt is None:
        return ""
    return dt.isoformat() + "Z"
