from rich.console import Console
from rich.panel import Panel
import questionary
from app.utils.constants import (
    ASSIGN_COLLABORATOR_TO_EVENT,
    CREATE_CUSTOMER,
    CREATE_EVENT,
    DISPLAY_MY_EVENTS,
    EVENT_WITHOUT_SUPPORT_COLLABORATOR,
    MODIFY_CUSTOMER,
    SIGNIN,
    SIGNUP,
    LOGOUT,
    CREATE_CONTRACT,
    UPDATE_MY_EVENTS,
    MODIFY_CONTRACT,
    MODIFY_COLLABORATOR,
    DELETE_COLLABORATOR,
    VIEW_CUSTOMERS,
)

console = Console()
texte = "[bold blue]\n Welcome to Epic Events, event management software \n[/bold blue]"


def render_main_menu():
    console.print(Panel(texte, expand=False))
    choice = questionary.select(
        "Make a choice:",
        choices=[SIGNIN, SIGNUP, LOGOUT],
    ).ask()
    return choice


def render_management_menu():
    console.print(Panel("[bold cyan]Management Menu[/bold cyan]", expand=False))
    choice = questionary.select(
        "Make a choice:",
        choices=[
            CREATE_CONTRACT,
            MODIFY_CONTRACT,
            MODIFY_COLLABORATOR,
            DELETE_COLLABORATOR,
            EVENT_WITHOUT_SUPPORT_COLLABORATOR,
            ASSIGN_COLLABORATOR_TO_EVENT,
            LOGOUT,
        ],
    ).ask()
    return choice


def render_support_menu():
    console.print(Panel("[bold cyan]Support Menu[/bold cyan]", expand=False))
    choice = questionary.select(
        "Make a choice:",
        choices=[DISPLAY_MY_EVENTS, UPDATE_MY_EVENTS, LOGOUT],
    ).ask()
    return choice


def render_sales_menu():
    console.print(Panel("[bold cyan]Sales Menu[/bold cyan]", expand=False))
    choice = questionary.select(
        "Make a choice:",
        choices=[
            CREATE_CUSTOMER,
            VIEW_CUSTOMERS,
            MODIFY_CUSTOMER,
            MODIFY_CONTRACT,
            CREATE_EVENT,
            LOGOUT,
        ],
    ).ask()
    return choice


def render_access_denied():
    console.print(
        "[bold red]Access denied. Please sign in to continue.[/bold red]"
    )