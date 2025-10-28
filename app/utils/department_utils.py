from app.models.department import Department


def get_departments(session) -> list[dict]:
    """
    Fetch all departments from the database

    Returns a list of dictionaries with department id and name
    """
    departments = session.query(Department).all()
    return [{"id": d.id, "name": d.name} for d in departments]
