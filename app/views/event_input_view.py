from rich.console import Console
from app.validators.event_validator import (
    is_end_date_after_start,
    is_valid_attendees,
    is_valid_date,
    is_valid_location,
    is_valid_notes,
    is_valid_start_date
)
from app.views.common_input_view import ask_if_update

console = Console()


def ask_location() -> str:
    while True:
        location = console.input("Enter event location: ")
        if is_valid_location(location):
            return location
        console.print(
            "[red]Location cannot be empty and must be at most 150 characters."
            "[/red]"
        )


def ask_attendees() -> str:
    while True:
        attendees = console.input("Enter event attendees: ")
        if is_valid_attendees(attendees):
            return attendees
        console.print("[red]Attendees must be a positive integer.[/red]")


def ask_notes() -> str:
    while True:
        notes = console.input("Enter event notes: ")
        if is_valid_notes(notes):
            return notes
        console.print(
            "[red]Notes cannot be empty and must be at most 500 characters."
            "[/red]"
        )


def ask_start_date() -> str:
    while True:
        start_date = console.input("Enter event start date (YYYY-MM-DD): ")
        if is_valid_start_date(start_date):
            return start_date
        console.print(
            "[red]Start date must be a valid date in YYYY-MM-DD format and "
            "cannot be in the past.[/red]"
        )


def ask_end_date() -> str:
    while True:
        end_date = console.input("Enter event end date (YYYY-MM-DD): ")
        if is_valid_date(end_date):
            return end_date
        console.print(
            "[red]End date must be a valid date in YYYY-MM-DD format.[/red]"
        )


def ask_event_modification(event_object) -> dict:
    console = Console()
    console.print("[bold green]Modify Event Information[/bold green]")

    event_updated = {}

    if ask_if_update("location", event_object.location):
        event_updated["location"] = ask_location()

    if ask_if_update("attendees", str(event_object.attendees)):
        event_updated["attendees"] = ask_attendees()

    if ask_if_update("notes", event_object.notes):
        event_updated["notes"] = ask_notes()

    if ask_if_update("start date", str(event_object.start_date)):
        event_updated["start_date"] = ask_start_date()

    if ask_if_update("end date", str(event_object.end_date)):
        event_updated["end_date"] = ask_end_date()

    start_date = str(event_updated.get("start_date", event_object.start_date))
    end_date = str(event_updated.get("end_date", event_object.end_date))

    while not is_end_date_after_start(
        start_date,
        end_date
    ):
        console.print(
            "[red]End date must be after or equal to start date.[/red]"
        )
        event_updated["end_date"] = ask_end_date()
        end_date = str(event_updated["end_date"])

    return event_updated
