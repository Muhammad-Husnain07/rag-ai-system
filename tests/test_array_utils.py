from app.utils.array_utils import flatten_list


def test_flatten_list_basic():
    assert flatten_list([[1, 2], [3]]) == [1, 2, 3]


def test_flatten_list_empty():
    assert flatten_list([]) == []


def test_flatten_list_mixed():
    assert flatten_list([1, [2], 3]) == [1, 2, 3]
