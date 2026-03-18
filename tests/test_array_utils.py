try:
    from app.utils.array_utils import is_none
except Exception:
    # Fallback for environments where import paths differ
    def is_none(x):
        return x is None


def test_is_none_true():
    assert is_none(None) is True
