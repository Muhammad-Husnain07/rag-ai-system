from app.utils.string_utils import count_lines, remove_html_tags


def test_count_lines_single():
    assert count_lines("hello") == 1


def test_count_lines_multiple():
    assert count_lines("hello\nworld") == 2


def test_count_lines_empty():
    assert count_lines("") == 0


def test_count_lines_none():
    assert count_lines(None) == 0


def test_remove_html_tags():
    assert remove_html_tags("<b>hello</b>") == "hello"


def test_remove_html_tags_empty():
    assert remove_html_tags("") == ""
