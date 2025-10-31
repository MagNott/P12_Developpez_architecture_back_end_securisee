import re


def is_valid_first_name(first_name) -> bool:
    return bool(first_name.strip()) and len(first_name) <= 50


def is_valid_last_name(last_name) -> bool:
    return bool(last_name.strip()) and len(last_name) <= 50


def is_valid_email(email: str) -> bool:
    email = email.strip()
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    # how this regex works:
    # ^[\w\.-]+ → start with one or more word characters, dots, or hyphens
    # @ → followed by an '@' symbol
    # [\w\.-]+ → followed by one or more word characters, dots, or hyphens
    # \. → followed by a dot
    # \w{2,} → followed by at least two word characters (the domain)
    # $ → end of the string
    return re.match(pattern, email) is not None


def is_valid_phone_number(phone_number) -> bool:
    cleaned = phone_number.replace(" ", "").replace("-", "")
    return cleaned.isdigit() and len(cleaned) == 10


def is_valid_login(login) -> bool:
    return bool(login.strip()) and len(login) <= 20


def is_valid_password_complexity(password: str) -> bool:

    pattern = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{12,}$'  # noqa: E501
    )
    # How this regex works:
    # (?=.*[a-z]) → at least one lowercase letter
    # (?=.*[A-Z]) → at least one uppercase letter
    # (?=.*\d) → at least one digit
    # (?=.*[@$!%*#?&]) → at least one special character
    # [A-Za-z\d@$!%*#?&]{12,} → at least 12 characters from the allowed types

    return bool(pattern.match(password)) and len(password) <= 100
