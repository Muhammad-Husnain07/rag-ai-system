from app.utils.size_utils import is_large_file


def test_is_large_file_true():
    assert is_large_file(11 * 1024 * 1024, threshold_mb=10) is True


def test_is_large_file_false():
    assert is_large_file(5 * 1024 * 1024, threshold_mb=10) is False
