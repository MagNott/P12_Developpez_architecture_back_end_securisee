from rich.console import Console
from rich.panel import Panel
import questionary
from app.models.customer import Customer
from app.views.user_input_view import (
    ask_first_name,
    ask_last_name,
    ask_email,
    ask_phone_number,
)
from app.views.customer_input_view import ask_company_name


def get_customer_info() -> dict:
    console = Console()
    console.print("[bold green]Create a customer[/bold green]")

    dict_customer_user = {}

    dict_customer_user["first_name"] = ask_first_name()
    dict_customer_user["last_name"] = ask_last_name()
    dict_customer_user["email"] = ask_email()
    dict_customer_user["phone_number"] = ask_phone_number()
    dict_customer_user["company_name"] = ask_company_name()

    return dict_customer_user


def render_view_all_customers(customers: list[Customer]):
    console = Console()
    console.print(
        Panel(
            "[bold yellow][Customer Controller] view_customers() called[/bold yellow]",
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


def render_choice_customer(customers: list[Customer]) -> str | None:
    console = Console()
    console.print(
        Panel(
            "[bold yellow][Customer Controller] read_customers() called[/bold yellow]",
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
        f"{customer.id}: {customer.first_name} {customer.last_name}"
        for customer in customers
    ]
    customer_choice = questionary.select(
        "Select a customer to view details:", choices=customer_choices
    ).ask()
    return customer_choice


def render_read_customer(customer_object):
    console = Console()
    console.print(
        Panel(
            "[bold yellow][Customer Controller] read_customers() called[/bold yellow]",
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
    console.print(f"[bold green]Customer Details:[/bold green]")
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
