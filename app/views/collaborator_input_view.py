import questionary
from rich.console import Console
from app.models.collaborator import Collaborator
from app.utils.department_utils import get_departments
from app.validators.collaborator_validators import (
    is_valid_login,
    is_valid_password_complexity,
)
from app.views.common_input_view import ask_if_update
from app.views.user_input_view import (
    ask_email,
    ask_first_name,
    ask_last_name,
    ask_phone_number
)

console = Console()


def ask_login() -> str:
    while True:
        login = console.input("Enter login (need to be unique): ")
        if is_valid_login(login):
            return login
        console.print("[red]Login cannot be empty[/red]")


def ask_password() -> str:
    while True:
        console.print(
            "[bold yellow]Password must contain at least:[/bold yellow]\n"
            "- 12 characters\n"
            "- One lowercase letter\n"
            "- One uppercase letter\n"
            "- One number\n"
            "- One special character (@$!%*#?&)"
        )
        password = console.input("Enter password: ", password=True)
        if is_valid_password_complexity(password):
            return password
        console.print("[red]Password need to be valid and not empty[/red]")


def ask_collaborator_modification(session, collaborator: Collaborator) -> dict:
    console = Console()
    console.print("[bold green]Modify Collaborator Information[/bold green]")

    collaborator_updated = {}

    if ask_if_update("first name", str(collaborator.first_name)):
        collaborator_updated["first_name"] = ask_first_name()
    if ask_if_update("last name", str(collaborator.last_name)):
        collaborator_updated["last_name"] = ask_last_name()
    if ask_if_update("email", str(collaborator.mail)):
        collaborator_updated["mail"] = ask_email()
    if ask_if_update("phone number", str(collaborator.phone_number)):
        collaborator_updated["phone_number"] = ask_phone_number()
    if ask_if_update("login", str(collaborator.login)):
        collaborator_updated["login"] = ask_login()
    if ask_if_update("password", str(collaborator.password)):
        collaborator_updated["password"] = ask_password()

    departments = get_departments(session)
    department_choices = [
        f"{dept['id']}: {dept['name']}" for dept in departments
    ]
    department_choice = questionary.select(
        "Select your department:", choices=department_choices
    ).ask()
    collaborator_updated["department_id"] = int(
        department_choice.split(":")[0]
        )
    # need to convert to int because questionary returns a string
    # need to split to get only the id part

    return collaborator_updated


def ask_confirm_delete(collaborator: Collaborator) -> bool:
    confirm = questionary.confirm(
        f"Are you sure you want to delete {collaborator.first_name} "
        f"{collaborator.last_name} (ID {collaborator.id})?"
    ).ask()
    return confirm is True
