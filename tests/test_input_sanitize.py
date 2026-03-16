from app.utils.input_sanitize import sanitize_input


def test_sanitize_input_basic():
    assert sanitize_input("  hello   WORLD \n") == "hello WORLD"


def test_sanitize_input_none():
    assert sanitize_input(None) == ""
