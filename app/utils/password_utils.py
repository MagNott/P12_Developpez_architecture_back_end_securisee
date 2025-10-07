import bcrypt


def hash_password(clear_password: str) -> str:
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(clear_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_password(clear_password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed value."""
    return bcrypt.checkpw(
        clear_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
