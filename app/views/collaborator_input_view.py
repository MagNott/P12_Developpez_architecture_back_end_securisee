from rich.console import Console
from app.validators.collaborator_validators import (
    is_valid_first_name,
    is_valid_last_name,
    is_valid_email,
    is_valid_phone_number,
    is_valid_login,
    is_valid_password
)

console = Console()


def ask_first_name() -> str:
    while True:
        first_name = console.input("Enter first name: ")
        if is_valid_first_name(first_name):
            return first_name
        console.print("[red]First name cannot be empty[/red]")


def ask_last_name() -> str:
    while True:
        last_name = console.input("Enter last name: ")
        if is_valid_last_name(last_name):
            return last_name
        console.print("[red]Last name cannot be empty[/red]")


def ask_email() -> str:
    while True:
        email = console.input("Enter email: ")
        if is_valid_email(email):
            return email
        console.print("[red]Invalid email. Enter a valid email address.[/red]")


def ask_phone_number() -> str:
    while True:
        phone_number = console.input("Enter phone number: ")
        if is_valid_phone_number(phone_number):
            return phone_number
        console.print("[red]Invalid phone number. Need 10 digits.[/red]")


def ask_login() -> str:
    while True:
        login = console.input("Enter login: ")
        if is_valid_login(login):
            return login
        console.print("[red]Login cannot be empty[/red]")


def ask_password() -> str:
    while True:
        password = console.input("Enter password: ", password=True)
        if is_valid_password(password):
            return password
        console.print("[red]Password cannot be empty[/red]")
