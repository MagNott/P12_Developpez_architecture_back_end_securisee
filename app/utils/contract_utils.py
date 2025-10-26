

from app.models.contract import Contract


def get_contracts(session) -> list[dict]:
    """
    Fetch all contracts from the database

    Returns a list of dictionaries with contract id and name
    """
    contracts = session.query(Contract).all()
    return [{"id": c.id, "name": f"Contract {c.id} - Customer {c.customer.first_name} {c.customer.last_name}"} for c in contracts]

