from rich.console import Console
from app.validators.collaborator_validators import (
    is_valid_login,
    is_valid_password,
)

console = Console()

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
