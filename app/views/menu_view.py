from rich.console import Console
from rich.panel import Panel
import questionary
from app.utils.constants import (
    ASSIGN_SUPPORT_COLLABORATOR_TO_EVENT,
    CREATE_COLLABORATOR,
    CREATE_CUSTOMER,
    CREATE_EVENT,
    DISPLAY_MY_EVENTS,
    FILTER_CONTRACTS_BY_STATUS,
    FILTER_CONTRACTS_NOT_FULLY_PAID,
    MODIFY_CUSTOMER,
    MODIFY_EVENT,
    READ_CONTRACT,
    READ_CUSTOMER,
    READ_EVENT,
    SIGNIN,
    SIGNUP,
    LOGOUT,
    CREATE_CONTRACT,
    MODIFY_CONTRACT,
    MODIFY_COLLABORATOR,
    DELETE_COLLABORATOR,
    VIEW_CONTRACTS,
    VIEW_CUSTOMERS,
    VIEW_EVENTS,
)

console = Console()
texte = (
    "[bold blue]\n"
    " Welcome to Epic Events, event management software \n"
    "[/bold blue]"
)


def render_main_menu():
    console.print(Panel(texte, expand=False))
    choice = questionary.select(
        "Make a choice:",
        choices=[SIGNIN, SIGNUP, LOGOUT],
    ).ask()
    return choice


def render_management_menu():
    console.print(Panel(
        "[bold cyan]Management Menu[/bold cyan]",
        expand=False
    ))
    choice = questionary.select(
        "Make a choice:",
        choices=[
            CREATE_COLLABORATOR,
            MODIFY_COLLABORATOR,
            DELETE_COLLABORATOR,
            VIEW_CUSTOMERS,
            READ_CUSTOMER,
            VIEW_CONTRACTS,
            READ_CONTRACT,
            CREATE_CONTRACT,
            MODIFY_CONTRACT,
            VIEW_EVENTS,
            READ_EVENT,
            ASSIGN_SUPPORT_COLLABORATOR_TO_EVENT,
            LOGOUT,
        ],
    ).ask()
    return choice


def render_support_menu():
    console.print(Panel("[bold cyan]Support Menu[/bold cyan]", expand=False))
    choice = questionary.select(
        "Make a choice:",
        choices=[
            VIEW_CUSTOMERS,
            READ_CUSTOMER,
            VIEW_CONTRACTS,
            READ_CONTRACT,
            VIEW_EVENTS,
            READ_EVENT,
            MODIFY_EVENT,
            DISPLAY_MY_EVENTS,
            LOGOUT
        ],
    ).ask()
    return choice


def render_sales_menu():
    console.print(Panel("[bold cyan]Sales Menu[/bold cyan]", expand=False))
    choice = questionary.select(
        "Make a choice:",
        choices=[
            CREATE_CUSTOMER,
            VIEW_CUSTOMERS,
            READ_CUSTOMER,
            MODIFY_CUSTOMER,
            VIEW_CONTRACTS,
            READ_CONTRACT,
            FILTER_CONTRACTS_BY_STATUS,
            FILTER_CONTRACTS_NOT_FULLY_PAID,
            MODIFY_CONTRACT,
            VIEW_EVENTS,
            READ_EVENT,
            CREATE_EVENT,
            LOGOUT,
        ],
    ).ask()
    return choice


def render_access_denied():
    console.print(
        "[bold red]Access denied. Please sign in to continue.[/bold red]"
    )
