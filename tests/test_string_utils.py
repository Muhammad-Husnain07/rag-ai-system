from app.utils.string_utils import count_lines


def test_count_lines_single():
    assert count_lines("hello") == 1


def test_count_lines_multiple():
    assert count_lines("hello\nworld") == 2


def test_count_lines_empty():
    assert count_lines("") == 0


def test_count_lines_none():
    assert count_lines(None) == 0
