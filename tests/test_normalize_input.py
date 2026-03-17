from app.utils.helpers import normalize_input


def test_normalize_input_basic():
    assert normalize_input("  HeLLo  WOrld  ") == "hello world"


def test_normalize_input_none():
    assert normalize_input(None) == ""
