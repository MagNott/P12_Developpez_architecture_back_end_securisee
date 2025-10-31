from rich.console import Console
from rich.panel import Panel
import questionary
from app.models.collaborator import Collaborator
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


def get_signup_info(session, connected_collaborator: Collaborator) -> dict:
    console = Console()
    console.print(
        Panel(
            "[bold yellow]Sign Up called [/bold yellow]",
            expand=False,
        )
    )

    dict_info_user = {}

    dict_info_user["first_name"] = ask_first_name()
    dict_info_user["last_name"] = ask_last_name()
    dict_info_user["email"] = ask_email()
    dict_info_user["phone_number"] = ask_phone_number()
    dict_info_user["login"] = ask_login()
    dict_info_user["password"] = ask_password()

    departments = get_departments(session)
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


def render_choice_collaborator(
        collaborators,
        connected_collaborator: Collaborator) -> str | None:
    console = Console()
    console.print(
        Panel(
            f"[bold yellow]Select a Collaborator called with "
            f"{connected_collaborator.first_name} "
            f"{connected_collaborator.last_name} - "
            f"{connected_collaborator.department.name}[/bold yellow]",
            expand=False
        )
    )

    if not collaborators:
        console.print("[bold red]No collaborators available.[/bold red]")
        return None

    collaborator_choices = [
        f"{collab.id}: {collab.first_name} {collab.last_name}"
        for collab in collaborators
    ]
    collaborator_choice = questionary.select(
        "Choose a collaborator:", choices=collaborator_choices
    ).ask()

    if collaborator_choice is None:
        return None

    return collaborator_choice


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
        f"Welcome back, {collaborator_found.first_name} "
        f"{collaborator_found.last_name}!"
    )


def show_signin_error():
    console = Console()
    console.print(
        "[bold red]Error during sign in. Check your login and password."
        "[/bold red]"
    )


def show_modified_success():
    console = Console()
    console.print("[bold green]Collaborator modified successfully!"
                  "[/bold green]")


def show_modified_error():
    console = Console()
    console.print("[bold red]Error during collaborator modification. "
                  "Try again.[/bold red]")


def show_error_commiting_to_db(e):
    console = Console()
    console.print(
        "[bold red]Error committing to the database. Please try again."
        "[/bold red]"
    )
    console.print(f"[red]Details: {e}[/red]")


def show_cannot_delete_self():
    console = Console()
    console.print(
        "[bold red]You cannot delete your own account.[/bold red]"
    )


def show_delete_success():
    console = Console()
    console.print(
        "[bold green]Collaborator deleted successfully![/bold green]"
    )


def show_delete_error():
    console = Console()
    console.print(
        "[bold red]Error deleting collaborator. Try again.[/bold red]"
    )


def show_log_out_success():
    console = Console()
    console.print("[bold green]Log out successful![/bold green]")
