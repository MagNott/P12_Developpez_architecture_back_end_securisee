from rich.console import Console


def ask_if_update(field_name: str, current_value: str) -> bool:
    console = Console()
    console.print(f"Current {field_name}: {current_value}")
    answer = input(f"Modify {field_name}? (y/N): ").lower()
    # Default to 'N' if the user just presses Enter because it's not y

    return answer == "y"