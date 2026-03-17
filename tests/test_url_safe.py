from app.utils.url_safe import is_safe_url


def test_is_safe_url_valid_https():
    assert is_safe_url("https://example.com")


def test_is_safe_url_valid_http_local():
    assert is_safe_url("http://localhost:8080")


def test_is_safe_url_invalid_scheme():
    assert not is_safe_url("ftp://example.com")


def test_is_safe_url_missing_domain():
    assert not is_safe_url("https:///path")
