from rich.console import Console
from rich.panel import Panel
import questionary
from app.utils.constants import SIGNIN, SIGNUP, LOGOUT

console = Console()

texte = "[bold blue]\n Welcome to Epic Events, event management software \n[/bold blue]"


def render_main_menu():
    console.print(Panel(texte, expand=False))
    return questionary.select(
            "Make a choice:",
            choices=[SIGNIN, SIGNUP, LOGOUT],
        ).ask()
