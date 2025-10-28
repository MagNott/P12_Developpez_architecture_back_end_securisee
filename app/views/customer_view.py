from rich.console import Console
from rich.panel import Panel
import questionary
from app.models.collaborator import Collaborator
from app.models.customer import Customer
from app.views.user_input_view import (
    ask_first_name,
    ask_last_name,
    ask_email,
    ask_phone_number,
)
from app.views.customer_input_view import ask_company_name


def get_customer_info(connected_collaborator: Collaborator) -> dict:
    console = Console()
    console.print(
        f"[bold green]Create a customer with "
        f"{connected_collaborator.first_name} "
        f"{connected_collaborator.last_name} - "
        f"{connected_collaborator.department.name}[/bold green]")

    dict_customer_user = {}

    dict_customer_user["first_name"] = ask_first_name()
    dict_customer_user["last_name"] = ask_last_name()
    dict_customer_user["email"] = ask_email()
    dict_customer_user["phone_number"] = ask_phone_number()
    dict_customer_user["company_name"] = ask_company_name()

    return dict_customer_user


def render_view_all_customers(customers: list[Customer],
                              connected_collaborator: Collaborator):
    console = Console()
    console.print(
        Panel(
            f"[bold yellow][Customer Controller] view_customers() called with "
            f"{connected_collaborator.first_name} "
            f"{connected_collaborator.last_name} - "
            f"{connected_collaborator.department.name}[/bold yellow]",
            expand=False,
        )
    )

    if not customers:
        console.print(
            Panel(
                "[bold red]No customers to display.[/bold red]",
                expand=False
            )
        )
        console.rule("", style="bold red")
        return
    for customer in customers:
        console.print(
            f"[bold green]- [/bold green] {customer.first_name} \
                {customer.last_name}"
        )
    console.rule("End of customer list", style="bold green")


def render_choice_customer(
        customers: list[Customer],
        connected_collaborator: Collaborator
) -> str | None:
    console = Console()
    console.print(
        Panel(
            f"[bold yellow][Customer Controller] read_customers() called with "
            f"{connected_collaborator.first_name} "
            f"{connected_collaborator.last_name} - "
            f"{connected_collaborator.department.name}[/bold yellow]",
            expand=False,
        )
    )

    if not customers:
        console.print(
            Panel(
                "[bold red]No customers to display.[/bold red]",
                expand=False
            )
        )
        console.rule("", style="bold red")
        return
    customer_choices = [
        f"{customer.id}: {customer.first_name} {customer.last_name} of sales "
        f"collaborator: {customer.collaborator.first_name} "
        f"{customer.collaborator.last_name}"
        for customer in customers
    ]
    customer_choice = questionary.select(
        "Select a customer to view details:", choices=customer_choices
    ).ask()
    return customer_choice


def render_read_customer(
        customer_object,
        connected_collaborator: Collaborator
):
    console = Console()
    console.print(
        Panel(
            f"[bold yellow][Customer Controller] read_customers() called with "
            f"{connected_collaborator.first_name} "
            f"{connected_collaborator.last_name} - "
            f"{connected_collaborator.department.name}[/bold yellow]",
            expand=False,
        )
    )

    if not customer_object:
        console.print(
            Panel(
                "[bold red]Customer not found.[/bold red]",
                expand=False
            ))
        console.rule("", style="bold red")
        return
    console.print("[bold green]Customer Details:[/bold green]")
    console.print(f"ID: {customer_object.id}")
    console.print(f"First Name: {customer_object.first_name}")
    console.print(f"Last Name: {customer_object.last_name}")
    console.print(f"Email: {customer_object.mail}")
    console.print(f"Phone Number: {customer_object.phone_number}")
    console.print(f"Company Name: {customer_object.company_name}")
    console.print(f"Creation Date: {customer_object.creation_date}")
    console.print(f"Last Update: {customer_object.last_update}")
    console.rule("End of customer details", style="bold green")


def show_created_customer_success():
    console = Console()
    console.print(
        Panel(
            "[bold green]Customer created successfully![/bold green]",
            expand=False
        )
    )


def show_created_customer_error():
    console = Console()
    console.print(
        Panel(
            "[bold red]Error creating customer. Please try again.[/bold red]",
            expand=False,
        )
    )


def show_modified_customer_success():
    console = Console()
    console.print(
        Panel(
            "[bold green]Customer modified successfully![/bold green]",
            expand=False
        )
    )


def show_modified_customer_error():
    console = Console()
    console.print(
        Panel(
            "[bold red]Error modifying customer. Please try again.[/bold red]",
            expand=False,
        )
    )
