from app.models.status import Status
from db import Session


def get_statuses() -> list[dict]:
    """
    Fetch all statuses from the database

    Returns a list of dictionaries with status id and name
    """
    session = Session()
    try:
        statuses = session.query(Status).all()
        return [{"id": s.id, "name": s.name} for s in statuses]
    finally:
        session.close()
