from app.utils.url_utils import is_valid_url, extract_domain


def test_is_valid_url():
    assert is_valid_url("https://example.com")
    assert is_valid_url("http://localhost:8000/test")
    assert not is_valid_url("not a url")


def test_extract_domain():
    assert extract_domain("https://example.com/path") == "example.com"
    assert extract_domain("http://localhost:8080/") == "localhost:8080"
    assert extract_domain("not a url") is None
