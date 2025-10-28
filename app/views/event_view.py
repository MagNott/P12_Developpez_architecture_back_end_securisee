from app.models.collaborator import Collaborator
from app.views.event_input_view import (
    ask_location,
    ask_notes,
    ask_attendees,
    ask_start_date,
    ask_end_date,
)
import questionary
from rich.console import Console
from rich.panel import Panel
from app.validators.event_validator import is_end_date_after_start


def get_event_info(
        session,
        filtered_contracts,
        connected_collaborator: Collaborator
) -> dict:
    console = Console()
    console.print(
        f"[bold green]Create an event with {connected_collaborator.first_name}"
        f" {connected_collaborator.last_name} - "
        f"{connected_collaborator.department.name}[/bold green]")

    dict_event = {}

    dict_event["location"] = ask_location()
    dict_event["attendees"] = ask_attendees()
    dict_event["notes"] = ask_notes()
    dict_event["start_date"] = ask_start_date()
    dict_event["end_date"] = ask_end_date()

    while not is_end_date_after_start(
        dict_event["start_date"], dict_event["end_date"]
    ):
        console.print("[red]End date must be after start date.[/red]")
        dict_event["end_date"] = ask_end_date()

    filtered_contracts = [
        f"{contract.id}: Contract for {contract.customer.first_name} "
        f"{contract.customer.last_name}"
        for contract in filtered_contracts
    ]
    contract_choice = questionary.select(
        "Select contract:", choices=filtered_contracts
    ).ask()
    dict_event["contract_id"] = int(contract_choice.split(":")[0])
    # need to convert to int because questionary returns a string
    # need to split to get only the id part

    return dict_event


def render_view_all_events(events, connected_collaborator: Collaborator):
    console = Console()
    console.print(
        Panel(
            f"[bold yellow][Event Controller] view_events() called with "
            f"{connected_collaborator.first_name} "
            f"{connected_collaborator.last_name} - "
            f"{connected_collaborator.department.name}[/bold yellow]",
            expand=False,
        )
    )

    if not events:
        console.print(Panel(
            "[bold red]No events to display.[/bold red]",
            expand=False)
        )
        console.rule("", style="bold red")
        return
    for event in events:
        console.print(
            f"[bold green]- [/bold green] Event ID: {event.id} "
            f"| location : {event.location} | Date: {event.start_date} "
            f"| Client: {event.contract.customer.first_name} "
            f"{event.contract.customer.last_name}"
        )
    console.rule("End of event list", style="bold green")


def render_choice_event(
        events,
        connected_collaborator: Collaborator
) -> str | None:
    console = Console()
    console.print(
        Panel(
            f"[bold yellow][Event Controller] read_event() called with "
            f"{connected_collaborator.first_name} "
            f"{connected_collaborator.last_name} - "
            f"{connected_collaborator.department.name}[/bold yellow]",
            expand=False,
        )
    )

    if not events:
        console.print(Panel("[bold red]No events to display.[/bold red]",
                            expand=False))
        console.rule("", style="bold red")
        return None

    event_choices = [
        f"{event.id}: {event.location} | {event.start_date} to "
        f"{event.end_date} | Client: {event.contract.customer.first_name} "
        f"{event.contract.customer.last_name}"
        for event in events
    ]
    event_choice = questionary.select(
        "Select an event to view details:", choices=event_choices
    ).ask()
    return event_choice


def render_view_event_details(
        event_object,
        connected_collaborator: Collaborator
):
    console = Console()
    console.print(
        Panel(
            f"[bold yellow][Event Controller] Event Details with "
            f"{connected_collaborator.first_name} "
            f"{connected_collaborator.last_name} - "
            f"{connected_collaborator.department.name}[/bold yellow]",
            expand=False,
        )
    )

    console.print(f"[bold green]Event ID:[/bold green] {event_object.id}")
    console.print(
        f"[bold green]Location:[/bold green] {event_object.location}"
    )
    console.print(
        f"[bold green]Attendees:[/bold green] {event_object.attendees}"
    )
    console.print(f"[bold green]Notes:[/bold green] {event_object.notes}")
    console.print(
        f"[bold green]Start Date:[/bold green] {event_object.start_date}"
    )
    console.print(
        f"[bold green]End Date:[/bold green] {event_object.end_date}"
    )
    console.print(
        f"[bold green]Contract:[/bold green] {event_object.contract_id} - "
        f"Client: {event_object.contract.customer.first_name} "
        f"{event_object.contract.customer.last_name}"
    )
    if event_object.collaborator_id:
        console.print(
            f"[bold green]Collaborator ID:[/bold green] "
            f"{event_object.collaborator_id} - "
            f"{event_object.collaborator.first_name} "
            f"{event_object.collaborator.last_name}"
        )

    console.rule("End of event details", style="bold green")


def render_choice_support_collaborator(
        support_collaborators,
        connected_collaborator: Collaborator
) -> str | None:
    console = Console()
    console.print(
        Panel(
            f"[bold yellow][Event Controller] Select Support Collaborator "
            f"with {connected_collaborator.first_name} "
            f"{connected_collaborator.last_name} - "
            f"{connected_collaborator.department.name}[/bold yellow]",
            expand=False,
        )
    )

    collaborator_choices = [
        f"{coll['id']}: {coll['name']}"
        for coll in support_collaborators
    ]
    collaborator_choice = questionary.select(
        "Select a support collaborator:", choices=collaborator_choices
    ).ask()
    return collaborator_choice


def render_view_my_events(events, connected_collaborator: Collaborator):
    console = Console()
    console.print(
        Panel(
            f"[bold yellow][Event Controller] display_my_events() called with "
            f"{connected_collaborator.first_name} "
            f"{connected_collaborator.last_name} - "
            f"{connected_collaborator.department.name}[/bold yellow]",
            expand=False,
        )
    )

    if not events:
        console.print(Panel("[bold red]No events to display.[/bold red]",
                            expand=False))
        console.rule("", style="bold red")
        return
    for event in events:
        console.print(
            f"[bold green]- [/bold green] Event ID: {event.id} "
            f" | location : {event.location} | Date: {event.start_date} | "
            f"Client: {event.contract.customer.first_name} "
            f"{event.contract.customer.last_name}"
        )
    console.rule("End of my event list", style="bold green")


def show_created_event_success():
    console = Console()
    console.print(
        Panel("[bold green]Event created successfully![/bold green]",
              expand=False)
    )


def show_created_event_error():
    console = Console()
    console.print(Panel("[bold red]Error creating event.[/bold red]",
                        expand=False))


def show_modified_event_success():
    console = Console()
    console.print(
        Panel("[bold green]Event modified successfully.[/bold green]",
              expand=False)
    )


def show_modified_event_error():
    console = Console()
    console.print(Panel("[bold red]Error modifying event.[/bold red]",
                        expand=False))


def show_events_without_support_collaborator(events):
    console = Console()
    console.print(
        Panel(
            "[bold yellow][Event Controller] Events without Support "
            "Collaborator[/bold yellow]",
            expand=False,
        )
    )

    if not events:
        console.print(
            Panel(
                "[bold red]No events without support collaborator.[/bold red]",
                expand=False,
            )
        )
        console.rule("", style="bold red")
        return


def show_assigned_event_success():
    console = Console()
    console.print(
        Panel(
            "[bold green]Support collaborator assigned to event successfully!"
            "[/bold green]",
            expand=False,
        )
    )


def show_assigned_event_error():
    console = Console()
    console.print(
        Panel(
            "[bold red]Error assigning support collaborator to event."
            "[/bold red]",
            expand=False,
        )
    )


def show_no_signed_contracts_available():
    console = Console()
    console.print(
        Panel(
            "[bold red]No signed contracts available for your clients."
            "[/bold red]",
            expand=False,
        )
    )


def show_no_contracts_available():
    console = Console()
    console.print(
        Panel(
            "[bold red]No signed contracts available for your clients."
            "[/bold red]",
            expand=False,
        )
    )
