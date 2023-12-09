from ducklingscript import CompileOptions

from pathlib import Path
from typing import Annotated, Optional
from rich import print
import typer
import yaml
import os

path_type = Annotated[
    Optional[Path],
    typer.Argument(
        help="Directory to place project (creates a new folder using the name)",
        file_okay=False,
        writable=True,
    ),
]


def new(
    name: Annotated[str, typer.Argument(help="Name of the project")],
    path: path_type = None,
):
    """
    Create a new project
    """
    config_name = "config.yaml"
    main_name = "main.txt"

    name = name.strip().lower().replace(" ", "-")
    for i in name:
        if i not in "abcdefghijklmnopqrstuvwxyz1234567890-":
            print_error(
                "Names must require only letters and numbers. If there are spaces, they are replaced with '-'. If there are any upper case letters, they are made lower case."
            )
            return

    if path is None:
        path = Path(os.getcwd())
    full_dir = path / name

    if not full_dir.exists():
        full_dir.mkdir(parents=True)
    else:
        print_error("Project dir already exists.")
        return

    config_file = full_dir / config_name
    with config_file.open("w") as f:
        f.write(yaml.dump(CompileOptions().to_dict()))

    main_file = full_dir / main_name
    with main_file.open("w") as f:
        f.write("STRING Hello, World!")

    print_success(f"Project successfully created!\n\n{full_dir.absolute()}")


def print_error(text: str | list[str]):
    new_line = "\n"
    if isinstance(text, str):
        text = [text]
    print(f"[bold red]---\n{new_line.join(text)} ⛔\n---[/bold red]")


def print_success(text: str | list[str]):
    new_line = "\n"
    if isinstance(text, str):
        text = [text]
    print(f"[bold green]---\n{new_line.join(text)} ✅\n---[/bold green]")
