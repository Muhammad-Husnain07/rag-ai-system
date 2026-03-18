from app.utils.misc import is_none


def test_is_none_true():
    assert is_none(None) is True


def test_is_none_false():
    assert is_none(0) is False
