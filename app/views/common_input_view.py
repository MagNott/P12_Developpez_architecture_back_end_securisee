import questionary
from rich.console import Console


def ask_if_update(field_name: str, current_value: str) -> bool:
    console = Console()
    console.print(f"Current {field_name}: {current_value}")
    response = questionary.confirm(
        f"Do you want to update {field_name}? (Current: {current_value})",
        default=False
    ).ask()

    return response
