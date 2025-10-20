from app.models.collaborator import Collaborator
from db import Session


def find_collaborator_by_login(user_login: str) -> Collaborator | None:
    """
    Find a collaborator by their login.

    Returns the Collaborator object if found, None otherwise.
    """
    session = Session()

    collaborator_found = (
        session.query(Collaborator).filter_by(login=user_login).first()
    )
    # .first()  returns None if no result is found
    return collaborator_found
