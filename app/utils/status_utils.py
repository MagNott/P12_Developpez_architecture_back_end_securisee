from app.models.status import Status


def get_statuses(session) -> list[dict]:
    """
    Fetch all statuses from the database

    Returns a list of dictionaries with status id and name
    """
    statuses = session.query(Status).all()
    return [{"id": s.id, "name": s.name} for s in statuses]
