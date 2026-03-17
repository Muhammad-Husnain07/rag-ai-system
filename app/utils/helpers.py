import re
from typing import List, Optional
from datetime import datetime


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent security issues."""
    filename = re.sub(r'[^\w\s.-]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    return filename[:255]


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    size = float(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def format_datetime(dt: Optional[datetime] = None) -> str:
    """Format datetime to ISO format."""
    if dt is None:
        dt = datetime.utcnow()
    return dt.isoformat() + 'Z'


def parse_datetime(dt_str: str) -> Optional[datetime]:
    """Parse datetime from ISO format string."""
    try:
        if dt_str.endswith('Z'):
            dt_str = dt_str[:-1]
        return datetime.fromisoformat(dt_str)
    except (ValueError, AttributeError):
        return None


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max length with suffix."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """Extract keywords from text."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()
    
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'can', 'this', 'that', 'these',
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which',
        'who', 'whom', 'whose', 'where', 'when', 'why', 'how', 'all', 'each',
        'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no'
    }
    
    words = [w for w in words if w not in stop_words and len(w) > 2]
    
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_words[:max_keywords]]


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength.
    Returns (is_valid, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"


def generate_random_string(length: int = 32) -> str:
    """Generate random string for tokens."""
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
def safe_get_env(key: str, default=None):
    """Return environment variable or default if not set.
    This helps centralize safe access to configuration values.
    """
    import os
    return os.environ.get(key, default)


def merge_dicts(a: dict, b: dict) -> dict:
    """Return a new dict that merges two dictionaries (shallow merge).
    Values from b override those in a when keys collide.
    """
    result = dict(a or {})
    if b:
        result.update(b)
    return result


def normalize_input(text: Optional[str]) -> str:
    """Normalize input by sanitizing and lowercasing if present."""
    from app.utils.input_sanitize import sanitize_input
    cleaned = sanitize_input(text)
    return cleaned.lower() if cleaned else ""
