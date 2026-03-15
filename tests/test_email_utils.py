import re

from app.utils.email_utils import is_valid_email


def test_is_valid_email():
    assert is_valid_email("test@example.com")
    assert is_valid_email("user.name+tag@domain.co.uk")
    assert not is_valid_email("invalid-email")
    assert not is_valid_email("@missing.local")
