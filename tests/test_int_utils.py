from app.utils.int_utils import safe_int_parse, safe_float_parse


def test_safe_int_parse_valid():
    assert safe_int_parse("123") == 123


def test_safe_int_parse_invalid():
    assert safe_int_parse("abc") == 0


def test_safe_int_parse_none_with_default():
    assert safe_int_parse(None, default=7) == 7

def test_safe_int_parse_negative():
    assert safe_int_parse("-42") == -42


def test_safe_float_parse_valid():
    assert safe_float_parse("3.14") == 3.14


def test_safe_float_parse_invalid():
    assert safe_float_parse("abc") == 0.0


def test_safe_float_parse_none_with_default():
    assert safe_float_parse(None, default=5.0) == 5.0
