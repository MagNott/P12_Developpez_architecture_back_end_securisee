from app.utils.password_utils import hash_password, verify_password


def test_hash_password_is_okay():
    """Test the hash_password function."""
    clear_password = "monSuperMotDePasse123!"
    hashed_password = hash_password(clear_password)
    assert isinstance(hashed_password, str)
    assert hashed_password != clear_password
    assert len(hashed_password) > 0


def test_verify_password_is_okay():
    """Test the verify_password function."""
    clear_password = "monSuperMotDePasse123!"
    hashed_password = hash_password(clear_password)
    assert verify_password(clear_password, hashed_password) is True
    assert verify_password("wrongPassword", hashed_password) is False
