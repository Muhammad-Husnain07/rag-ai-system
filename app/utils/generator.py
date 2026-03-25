import secrets
import string
import uuid


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


def generate_uuid() -> str:
    """Generate a random UUID4 string."""
    return str(uuid.uuid4())


def generate_batch_id() -> str:
    """Generate a batch ID with timestamp prefix."""
    from datetime import datetime
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"batch_{timestamp}_{generate_random_string(8)}"


def generate_token(length: int = 32) -> str:
    """Generate a secure random token."""
    return secrets.token_urlsafe(length)
