import questionary
from rich.console import Console
from rich.panel import Panel

from app.models.collaborator import Collaborator
from app.views.contract_input_view import (ask_contract_amount,
                                           ask_contract_amount_due)


def get_contract_info(session, connected_collaborator: Collaborator) -> dict:
    console = Console()
    console.print(f"[bold green]Create a contract for "
                  f"{connected_collaborator.first_name} "
                  f"{connected_collaborator.last_name} - "
                  f"{connected_collaborator.department.name}[/bold green]")

    dict_contract = {}

    dict_contract["contract_amount"] = ask_contract_amount()
    dict_contract["amount_due"] = ask_contract_amount_due()
    while not dict_contract["amount_due"] <= dict_contract["contract_amount"]:
        console.print(
            "[red]Amount due must be less than or equal to contract amount."
            "[/red]"
        )
        dict_contract["amount_due"] = ask_contract_amount_due()

    return dict_contract


def render_view_all_contracts(
        contracts,
        connected_collaborator: Collaborator
):
    console = Console()
    console.print(
        Panel(
            f"[bold yellow][Contract Controller] view_contracts() called with "
            f"{connected_collaborator.first_name} "
            f"{connected_collaborator.last_name} - "
            f"{connected_collaborator.department.name}[/bold yellow]",
            expand=False,
        )
    )

    if not contracts:
        console.print(
            Panel("[bold red]No contracts to display.[/bold red]",
                  expand=False)
        )
        console.rule("", style="bold red")
        return
    for contract in contracts:
        console.print(
            f"[bold green]- [/bold green] Contract ID: {contract.id} "
            f"| Client : {contract.customer.id} "
            f"{contract.customer.first_name} {contract.customer.last_name} "
            f"| Amount: {contract.contract_amount} | "
            f"Amount due: {contract.amount_due}"
        )
    console.rule("End of contract list", style="bold green")


def render_choice_contract(
        contracts: list,
        connected_collaborator: Collaborator
) -> str | None:
    console = Console()
    console.print(
        Panel(
            f"[bold yellow][Contract Controller] read_contracts() called with "
            f"{connected_collaborator.first_name} "
            f"{connected_collaborator.last_name} - "
            f"{connected_collaborator.department.name}[/bold yellow]",
            expand=False,
        )
    )

    if not contracts:
        console.print(
            Panel("[bold red]No contracts available.[/bold red]", expand=False)
        )
        console.rule("", style="bold red")
        return None

    contract_choices = [
        f"{contract.id} : (Contract number) of customer : "
        f"{contract.customer.first_name} {contract.customer.last_name} | "
        f"Amount: {contract.contract_amount} of sales collaborator: "
        f"{contract.customer.collaborator.first_name} "
        f"{contract.customer.collaborator.last_name}"
        for contract in contracts
    ]
    contract_choice = questionary.select(
        "Select a contract:", choices=contract_choices
    ).ask()
    return contract_choice


def render_read_contract(
        contract_object,
        connected_collaborator: Collaborator
):
    console = Console()
    console.print(
        Panel(
            f"[bold yellow][Contract Controller] render_read_contract() called"
            f" with {connected_collaborator.first_name} "
            f"{connected_collaborator.last_name} - "
            f"{connected_collaborator.department.name}[/bold yellow]",
            expand=False,
        )
    )

    if not contract_object:
        console.print(Panel(
            "[bold red]Contract not found.[/bold red]",
            expand=False
        ))
        console.rule("", style="bold red")
        return

    console.print(
        f"[bold green]Contract ID:[/bold green] {contract_object.id}"
    )
    console.print(
        f"[bold green]Client:[/bold green] "
        f"{contract_object.customer.first_name} "
        f"{contract_object.customer.last_name} "
        f"(ID {contract_object.customer.id})"
    )
    console.print(
        f"[bold green]Contract Amount:[/bold green] "
        f"{contract_object.contract_amount}"
    )
    console.print(
        f"[bold green]Amount Due:[/bold green] "
        f"{contract_object.amount_due}"
    )
    console.print(
        f"[bold green]Creation Date:[/bold green] "
        f"{contract_object.creation_date}"
    )
    console.print(
        f"[bold green]Status:[/bold green] {contract_object.status.name}"
    )
    console.rule("End of contract details", style="bold green")


def render_choice_status_contracts(status_choices: list) -> str | None:
    console = Console()
    console.print(
        Panel(
            "[bold yellow][Contract Controller] filter_contracts_by_status() "
            "called[/bold yellow]",
            expand=False,
        )
    )
    status_choice = questionary.select(
        "Select status to filter contracts:", choices=status_choices
    ).ask()
    return status_choice


def show_created_contract_success():
    console = Console()
    console.print(
        Panel(
            "[bold green]Contract created successfully.[/bold green]",
            expand=False)
    )


def show_created_contract_error():
    console = Console()
    console.print(Panel(
        "[bold red]Error creating contract.[/bold red]",
        expand=False))


def show_modified_contract_success():
    console = Console()
    console.print(
        Panel(
            "[bold green]Contract modified successfully.[/bold green]",
            expand=False)
    )


def show_modified_contract_error():
    console = Console()
    console.print(Panel(
        "[bold red]Error modifying contract.[/bold red]",
        expand=False))
