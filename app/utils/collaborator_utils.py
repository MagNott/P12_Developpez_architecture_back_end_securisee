from app.models.collaborator import Collaborator
from db import Session
from sqlalchemy.orm import joinedload


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


def get_collaborators() -> list[dict]:
    """
    Fetch all collaborators from the database

    Returns a list of dictionaries with collaborator id and name
    """
    session = Session()
    try:
        collaborators = (
            session.query(Collaborator)
            .options(joinedload(Collaborator.department))
            # Need to filter by department name in view
            .all()
        )
        return [{"id": c.id,
                 "name": f"{c.first_name} {c.last_name}",
                 "departement": c.department.name
                 } for c in collaborators]
    finally:
        session.close()
