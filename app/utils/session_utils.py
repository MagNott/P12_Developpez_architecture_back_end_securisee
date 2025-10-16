import jwt
import datetime
import os
from typing import cast
from app.utils.collaborator_utils import find_collaborator_by_login
from app.models.collaborator import Collaborator
from app.models.department import Department

# NEED TO PROTECT THE SECRET KEY BETTER AFTER
SECRET_KEY = "ma_cle_secrete"
SESSION_FILE = ".session"


def generate_token(collaborator: Collaborator) -> str:
    """
    Create a JWT token for a collaborator with an expiration time
    Args:
        collaborator (Collaborator): The collaborator for whom to create the
        token
    Returns:
        str: The generated JWT token
    """
    today = datetime.datetime.now()
    payload = {
        "login": collaborator.login,
        "exp": today + datetime.timedelta(minutes=1),
        "department": collaborator.department.name,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def save_token(token: str) -> None:
    """
    Save the token in a local text file (.session)
    Args:
        token (str): The JWT token to save
    """
    with open(SESSION_FILE, "w", encoding="utf-8") as file:
        file.write(token)


def is_authenticated() -> Collaborator | bool:
    """
    Check if the user is authenticated by verifying the token's existence and
    validity

    Returns:
        Collaborator | bool: The authenticated collaborator or False if
        not authenticated
    """
    if not os.path.exists(SESSION_FILE):
        return False
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as file:
            token = file.read()
        collaborator_data = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_exp": True},
        )
        collaborator = find_collaborator_by_login(collaborator_data["login"])
        if not collaborator:
            return False
        return collaborator
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False


def get_authenticated_department() -> Department | None:
    """Get the department of the authenticated collaborator.

    Returns:
        str | None: The name of the department or None if not authenticated.
    """
    collaborator = is_authenticated()
    if not collaborator:
        return None
    collaborator = cast(Collaborator, collaborator)
    # Help for Pylance - import cast from typing
    department = collaborator.department
    return department
