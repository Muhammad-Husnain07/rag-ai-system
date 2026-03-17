from app.utils.json_pretty import pretty_json


def test_pretty_json_basic():
    data = {"b": 1, "a": 2}
    s = pretty_json(data, indent=2)
    assert isinstance(s, str)
    assert "\n" in s
    assert '"a": 2' in s  # keys are sorted by default
