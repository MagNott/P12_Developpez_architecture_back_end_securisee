from app.validators.contract_validators import (
    is_valid_contract_amount,
    is_valid_contract_amount_due,
)


def test_valid_contract_amount():
    assert is_valid_contract_amount("0") is True
    assert is_valid_contract_amount("100.50") is True
    assert is_valid_contract_amount("999999") is True


def test_invalid_contract_amount():
    assert is_valid_contract_amount("-1") is False
    assert is_valid_contract_amount("abc") is False
    assert is_valid_contract_amount("") is False
    assert is_valid_contract_amount(" ") is False


def test_valid_contract_amount_due():
    assert is_valid_contract_amount_due("0") is True
    assert is_valid_contract_amount_due("250.75") is True
    assert is_valid_contract_amount_due("5000") is True


def test_invalid_contract_amount_due():
    assert is_valid_contract_amount_due("-10") is False
    assert is_valid_contract_amount_due("hello") is False
    assert is_valid_contract_amount_due("") is False
    assert is_valid_contract_amount_due("   ") is False
