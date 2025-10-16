import pytest
from app.validators.collaborator_validators import (
    is_valid_first_name,
    is_valid_last_name,
    is_valid_email,
    is_valid_phone_number,
    is_valid_login,
    is_valid_password,
)


def test_first_name_should_be_valid_when_normal_string():
    assert is_valid_first_name("Jean") is True


@pytest.mark.parametrize("first_name", ["", "   "])
def test_first_name_should_be_not_valid_when_empty_string_or_whitespace(
    first_name,
):
    assert is_valid_first_name(first_name) is False


def test_last_name_should_be_valid_when_normal_string():
    assert is_valid_last_name("Dupont") is True


@pytest.mark.parametrize("last_name", ["", "   "])
def test_last_name_should_be_not_valid_when_empty_string_or_whitespace(
    last_name,
):
    assert is_valid_last_name(last_name) is False


def test_email_should_be_valid_when_proper_format():
    assert is_valid_email("test@example.com") is True


@pytest.mark.parametrize("email", ["testexample.com", "test@.com"])
def test_email_should_be_not_valid_when_missing_at_symbol_or_domain(email):
    assert is_valid_email(email) is False


def test_phone_number_should_be_valid_when_10_digits():
    assert is_valid_phone_number("0123456789") is True


@pytest.mark.parametrize(
    "phone_number", ["012345678", "01234567890", "01234abcde"]
)
def test_phone_number_should_be_not_valid(phone_number):
    assert is_valid_phone_number(phone_number) is False


def test_login_should_be_valid_when_normal_string():
    assert is_valid_login("user123") is True


@pytest.mark.parametrize("login", ["", "   "])
def test_login_should_be_not_valid_when_empty_string_or_whitespace(login):
    assert is_valid_login(login) is False


def test_password_should_be_valid_when_normal_string():
    assert is_valid_password("securepassword") is True


@pytest.mark.parametrize("password", ["", "   "])
def test_password_should_be_not_valid_when_empty_string_or_whitespace(
    password,
):
    assert is_valid_password(password) is False
