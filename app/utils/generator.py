import secrets
import string


def generate_random_string(length: int = 32) -> str:
    """Generate a random alphanumeric string."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_random_hex(length: int = 32) -> str:
    """Generate a random hex string."""
    return secrets.token_hex(length // 2 + 1)[:length]


def generate_api_key() -> str:
    """Generate an API key format."""
    return f"rag_{generate_random_string(40)}"
