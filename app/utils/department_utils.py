from app.models.department import Department
from db import SessionLocal


def get_departments() -> list[dict]:
    session = SessionLocal()
    try:
        departments = session.query(Department).all()
        return [{"id": d.id, "name": d.name} for d in departments]
    finally:
        session.close()
