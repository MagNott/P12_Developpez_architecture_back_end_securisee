

from app.utils.contract_utils import get_contracts


def test_get_contract_success(
        db_session,
        fake_contracts
):
    contracts = get_contracts(db_session)

    assert len(contracts) == len(fake_contracts)
