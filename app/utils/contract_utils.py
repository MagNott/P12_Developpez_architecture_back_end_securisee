

from app.models.contract import Contract
from db import Session


def get_contracts() -> list[dict]:
    """
    Fetch all contracts from the database

    Returns a list of dictionaries with contract id and name
    """
    session = Session()
    try:
        contracts = session.query(Contract).all()
        return [{"id": c.id, "name": f"Contract {c.id} - Customer {c.customer.first_name} {c.customer.last_name}"} for c in contracts]
    finally:
        session.close()
