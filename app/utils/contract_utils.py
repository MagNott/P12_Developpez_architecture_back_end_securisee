from app.models.contract import Contract


def get_contracts(session) -> list[Contract]:
    """
    Fetch all contracts from the database

    Returns a list of dictionaries with contract id and name
    """
    contracts = session.query(Contract).all()
    return contracts
