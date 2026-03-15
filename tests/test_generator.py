from app.utils.generator import generate_random_string, generate_random_hex, generate_api_key


def test_generate_random_string_length():
    s = generate_random_string(16)
    assert isinstance(s, str) and len(s) == 16


def test_generate_random_hex_length():
    h = generate_random_hex(32)
    assert isinstance(h, str) and len(h) == 32


def test_generate_api_key_format():
    k = generate_api_key()
    assert isinstance(k, str) and k.startswith("rag_")
