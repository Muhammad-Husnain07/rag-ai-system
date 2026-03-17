from app.utils.number_utils import is_numeric


def test_is_numeric_true():
    assert is_numeric("123.45")
    assert is_numeric("-77")


def test_is_numeric_false():
    assert not is_numeric("abc")
    assert not is_numeric(123)  # non-string input should be treated as not numeric
