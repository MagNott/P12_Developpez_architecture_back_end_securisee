import hashlib
import os
import sentry_sdk


def hash_anonymize(clear_string: str) -> str:
    """
    Hash and anonymize a string using SHA-256 with a pepper.
    """
    try:
        pepper = os.getenv("PEPPER")
        if not pepper:
            raise ValueError("PEPPER environment variable is not set.")
    except ValueError as e:
        sentry_sdk.capture_exception(e)
        sentry_sdk.flush()
        raise

    hashed_string = clear_string + pepper

    return hashlib.sha256(hashed_string.encode()).hexdigest()[:12]
