from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel

from ..compiler import BaseCommand
from ..compiler import command_palette

from .utils import format_name, separate_capitals


def all():
    """
    Show all available commands for
    DucklingScript.

    🐬 - Means flipper only command
    """
    console = Console()

    commands = [format_content(i) for i in command_palette]
    sorted_commands = sorted(commands, key=lambda a: a[0])

    renderables = [
        Panel(i[1], expand=True, title=i[0], subtitle="~o~o~o~")
        for i in sorted_commands
    ]

    console.print(Columns(renderables, padding=(1, 1)))


def format_content(command: type[BaseCommand]) -> tuple[str, str]:
    name = f"[bold]{format_name(command)}[/bold]"

    names_str = ", ".join(command.names)
    names = (names_str[:30] + "..") if len(names_str) > 30 else names_str
    return (
        name,
        f"[orchid]{names}[/orchid]\n[deep_sky_blue3]{separate_capitals(command.__base__.__name__)}[/deep_sky_blue3]",
    )


# def format_name(command: type[BaseCommand]):
#     name: str = separate_capitals(command.__name__).lower()
#     name = name.removeprefix("flipper ")
#     if command.flipper_only:
#         name+= " 🐬"

#     return name.title()

# def separate_capitals(text: str):
#     return re.sub(r"(\w)([A-Z])", r"\1 \2", text)
