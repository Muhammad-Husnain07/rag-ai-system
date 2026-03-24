import re


def is_valid_url(url: str) -> bool:
    """Check if a string is a valid URL."""
    url_pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE
    )
    return url_pattern.match(url) is not None


def extract_domain(url: str) -> str | None:
    """Extract domain from URL."""
    match = re.search(r'https?://([^/]+)', url)
    return match.group(1) if match else None


def extract_path(url: str) -> str:
    """Extract path from URL."""
    from urllib.parse import urlparse
    return urlparse(url).path


def extract_query_params(url: str) -> dict:
    """Extract query parameters from URL as a dictionary."""
    from urllib.parse import urlparse, parse_qs
    return dict(parse_qs(urlparse(url).query))
