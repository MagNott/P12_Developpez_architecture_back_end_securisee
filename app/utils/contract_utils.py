from app.models.contract import Contract


def get_contracts(session) -> list[Contract]:
    """
    Fetch all contracts from the database

    Returns a list objects contrtacts
    """
    contracts = session.query(Contract).all()
    return contracts
