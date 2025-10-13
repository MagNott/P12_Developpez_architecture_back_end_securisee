import re


def is_valid_first_name(first_name) -> bool:
    return bool(first_name.strip()) and len(first_name) <= 50


def is_valid_last_name(last_name) -> bool:
    return bool(last_name.strip()) and len(last_name) <= 50


def is_valid_email(email: str) -> bool:
    email = email.strip()
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None


def is_valid_phone_number(phone_number) -> bool:
    cleaned = phone_number.replace(" ", "").replace("-", "")
    return cleaned.isdigit() and len(cleaned) == 10


def is_valid_login(login) -> bool:
    return bool(login.strip()) and len(login) <= 20


def is_valid_password(password) -> bool:
    return bool(password.strip()) and len(password) <= 100
