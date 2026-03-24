import re
from typing import Optional


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def truncate(text: str, length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length."""
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix


def truncate_words(text: str, word_limit: int = 50, suffix: str = "...") -> str:
    """Truncate text to specified number of words."""
    words = text.split()
    if len(words) <= word_limit:
        return text
    return ' '.join(words[:word_limit]) + suffix


def remove_extra_spaces(text: str) -> str:
    """Remove extra whitespace from text."""
    return ' '.join(text.split())


def extract_urls(text: str) -> list:
    """Extract URLs from text."""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(url_pattern, text)


def mask_email(email: str) -> str:
    """Mask email address for privacy."""
    if '@' not in email:
        return email
    
    local, domain = email.split('@')
    if len(local) <= 2:
        masked_local = local[0] + '*'
    else:
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
    
    return f"{masked_local}@{domain}"


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def count_chars(text: str, include_spaces: bool = True) -> int:
    """Count characters in text."""
    if include_spaces:
        return len(text)
    return len(text.replace(' ', ''))


def count_vowels(text: str) -> int:
    """Count vowels (a, e, i, o, u) in the text, case-insensitive."""
    if not text:
        return 0
    return sum(1 for ch in text.lower() if ch in 'aeiou')


def count_lines(text: str) -> int:
    """Count lines in text."""
    if not text:
        return 0
    return len(text.splitlines())


def remove_html_tags(text: str) -> str:
    """Remove HTML tags from text."""
    return re.sub(r'<[^>]+>', '', text)


def reverse_string(text: str) -> str:
    """Reverse a string."""
    return text[::-1]


def remove_special_chars(text: str) -> str:
    """Remove special characters, keep only alphanumeric and spaces."""
    return re.sub(r'[^A-Za-z0-9\s]', '', text)


def starts_with(text: str, prefix: str) -> bool:
    """Check if text starts with the given prefix."""
    return text.startswith(prefix)


def ends_with(text: str, suffix: str) -> bool:
    """Check if text ends with the given suffix."""
    return text.endswith(suffix)


def contains_substring(text: str, substring: str) -> bool:
    """Check if text contains the given substring."""
    return substring in text


def to_snake_case(text: str) -> str:
    """Convert text to snake_case."""
    text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', text)
    text = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', text)
    return text.lower().replace(' ', '_').replace('-', '_')
