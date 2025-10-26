from app.validators.customer_validators import is_valid_company_name


def test_is_valid_company_name():

    assert is_valid_company_name("Valid Company") is True
    assert is_valid_company_name("  ") is False
    assert is_valid_company_name("") is False
    assert is_valid_company_name("A" * 101) is False
    assert is_valid_company_name("A" * 100) is True
