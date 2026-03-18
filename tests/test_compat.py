from app.utils.compat import ensure_str


def test_ensure_str_none():
    assert ensure_str(None) == ""


def test_ensure_str_value():
    assert ensure_str(123) == "123"
