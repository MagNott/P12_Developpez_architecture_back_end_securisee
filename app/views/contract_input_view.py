from rich.console import Console

from app.models.contract import Contract
from app.models.status import Status
from app.views.common_input_view import ask_if_update
import questionary

from app.validators.contract_validators import (
    is_valid_contract_amount,
    is_valid_contract_amount_due
)

console = Console()


def ask_contract_amount() -> float:
    while True:
        amount_str = console.input("Enter contract amount: ")
        if is_valid_contract_amount(amount_str):
            return float(amount_str)
        console.print("[red]Amount must be non-negative.[/red]")


def ask_contract_amount_due() -> float:
    while True:
        amount_due_str = console.input("Enter contract amount due: ")
        if is_valid_contract_amount_due(amount_due_str):
            return float(amount_due_str)
        console.print("[red]Amount due must be non-negative.[/red]")


def ask_status_change(statuses: list[dict]) -> int | None:
    status_choices = [f"{status['id']}: {status['name']}"
                      for status in statuses]
    choice = questionary.select(
        "Select a new status:", choices=status_choices
    ).ask()

    if choice:
        return int(choice.split(":")[0])
    return None


def ask_contract_modification(
    contract_object: Contract, current_status: Status, statuses: list[dict]
) -> dict:
    console = Console()
    console.print("[bold green]Modify Contract Information[/bold green]")

    contract_updated = {}

    if ask_if_update("contract amount", str(contract_object.contract_amount)):
        contract_updated["contract_amount"] = ask_contract_amount()
    if ask_if_update("amount due", str(contract_object.amount_due)):
        contract_updated["amount_due"] = ask_contract_amount_due()
    if ask_if_update("status", str(current_status.name)):
        new_status_id = ask_status_change(statuses)
        if new_status_id:
            contract_updated["status_id"] = new_status_id

    return contract_updated
