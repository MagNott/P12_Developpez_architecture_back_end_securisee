import hashlib
import os

import pytest
from app.utils.security_utils import hash_anonymize


def test_hash_anonymize_success():
    clear_string = "test_string"
    hashed = hash_anonymize(clear_string)

    pepper = os.getenv("PEPPER", "")

    # Ensure that the hash is consistent
    expected_hash = hashlib.sha256(
        (clear_string + pepper).encode()
    ).hexdigest()[:12]
    assert hashed == expected_hash
    assert isinstance(hashed, str)
    assert len(hashed) == 12
    # SHA-256 hash truncated to 12 characters


def test_hash_anonymize_no_pepper(monkeypatch):
    monkeypatch.delenv("PEPPER", raising=False)

    clear_string = "test_string_no_pepper"

    try:
        hash_anonymize(clear_string)
    except ValueError as e:
        assert str(e) == "PEPPER environment variable is not set."
    else:
        assert False, "ValueError was not raised when PEPPER is missing."


@pytest.mark.parametrize("input_string", [
    "",
    "!@#$%^&*()_+-=[]{}|;':,.<>/?`~",
])
def test_hash_anonymize_different_type_string(input_string):
    clear_string = input_string
    hashed = hash_anonymize(clear_string)

    pepper = os.getenv("PEPPER", "")

    expected_hash = hashlib.sha256(
        (clear_string + pepper).encode()
    ).hexdigest()[:12]
    assert hashed == expected_hash
    assert isinstance(hashed, str)
    assert len(hashed) == 12
    # SHA-256 hash truncated to 12 characters
