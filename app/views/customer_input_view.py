from rich.console import Console
from app.validators.customer_validators import (
    is_valid_company_name,
)
from app.models.collaborator import Collaborator
from app.models.customer import Customer
from app.views.user_input_view import (
    ask_first_name,
    ask_last_name,
    ask_email,
    ask_phone_number,
)
import questionary


def ask_company_name() -> str:
    console = Console()
    while True:
        company_name = console.input("Enter company name: ")
        if is_valid_company_name(company_name):
            return company_name
        console.print("[red]Company name cannot be empty[/red]")


def ask_if_update(field_name: str, current_value: str) -> bool:
    console = Console()
    console.print(f"Current {field_name}: {current_value}")
    answer = input(f"Modify {field_name}? (y/N): ").lower()
    # Default to 'N' if the user just presses Enter because it's not y

    return answer == "y"


def ask_commercial_change(sales_collaborators: list[Collaborator]) -> int | None:
    sales_choices = [
        f"{sales_collaborator.id}: \
        {sales_collaborator.first_name} {sales_collaborator.last_name}"
        for sales_collaborator in sales_collaborators
    ]
    choice = questionary.select("Select a commercial:", choices=sales_choices).ask()

    if choice:
        return int(choice.split(":")[0])
    return None


def ask_customer_modification(
    customer_object: Customer,
    current_commercial_name: str,
    sales_collaborators: list[Collaborator],
) -> dict:
    console = Console()
    console.print("[bold green]Modify Customer Information[/bold green]")

    customer_updated = {}

    if ask_if_update("first name", str(customer_object.first_name)):
        customer_updated["first_name"] = ask_first_name()

    if ask_if_update("last name", str(customer_object.last_name)):
        customer_updated["last_name"] = ask_last_name()

    if ask_if_update("email", str(customer_object.mail)):
        customer_updated["email"] = ask_email()

    if ask_if_update("phone number", str(customer_object.phone_number)):
        customer_updated["phone_number"] = ask_phone_number()

    if ask_if_update("company name", str(customer_object.company_name)):
        customer_updated["company_name"] = ask_company_name()

    if ask_if_update("commercial", current_commercial_name):
        new_commercial_id = ask_commercial_change(sales_collaborators)
        if new_commercial_id:
            customer_updated["commercial_id"] = new_commercial_id

    return customer_updated
