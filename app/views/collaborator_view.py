from rich.console import Console
import questionary
from app.utils.department_utils import get_departments
from app.views.user_input_view import (
    ask_first_name,
    ask_last_name,
    ask_email,
    ask_phone_number)
from app.views.collaborator_input_view import (
    ask_login,
    ask_password,
)


def get_signup_info() -> dict:
    console = Console()
    console.print("[bold green]Sign Up[/bold green]")

    dict_info_user = {}

    dict_info_user["first_name"] = ask_first_name()
    dict_info_user["last_name"] = ask_last_name()
    dict_info_user["email"] = ask_email()
    dict_info_user["phone_number"] = ask_phone_number()
    dict_info_user["login"] = ask_login()
    dict_info_user["password"] = ask_password()

    departments = get_departments()
    department_choices = [
        f"{dept['id']}: {dept['name']}" for dept in departments
    ]
    department_choice = questionary.select(
        "Select your department:", choices=department_choices
    ).ask()
    dict_info_user["department_id"] = int(department_choice.split(":")[0])
    # need to convert to int because questionary returns a string
    # need to split to get only the id part
    return dict_info_user


def show_signup_success():
    console = Console()
    console.print("[bold green]Sign up successful![/bold green]")


def show_signup_error():
    console = Console()
    console.print("[bold red]Error during sign up. Try again.[/bold red]")


def show_signin_success(collaborator_found):
    console = Console()
    console.print("[bold green]Sign in successful![/bold green]")
    console.print(
        f"Welcome back, {collaborator_found.first_name} {collaborator_found.last_name}!"
    )


def show_signin_error():
    console = Console()
    console.print(
        "[bold red]Error during sign in. Check your login and password.[/bold red]"
    )
