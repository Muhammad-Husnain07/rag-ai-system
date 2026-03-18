from app.utils.json_utils import to_json


def test_to_json_basic():
    data = {"a": 1, "b": 2}
    s = to_json(data)
    assert isinstance(s, str) and '"a": 1' in s
