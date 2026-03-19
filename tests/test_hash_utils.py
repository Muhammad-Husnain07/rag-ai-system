from app.utils.hash_utils import sha256_hexdigest, md5_hexdigest


def test_sha256():
    result = sha256_hexdigest("hello")
    assert len(result) == 64


def test_md5():
    result = md5_hexdigest("hello")
    assert len(result) == 32


def test_none_input():
    assert len(sha256_hexdigest(None)) == 64
    assert len(md5_hexdigest(None)) == 32
