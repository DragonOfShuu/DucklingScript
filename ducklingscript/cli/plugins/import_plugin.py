from typing import Annotated
import typer
from pathlib import Path

from .app import app

@app.command(name="import", help="Import a DucklingScript plugin from a directory")
def import_plugin(
    path: Annotated[Path, typer.Argument(help="Path to the plugin file")],
):
    """
    Import a DucklingScript plugin from a directory.
    """
    # Check if the file exists
    if not Path(path).exists():
        raise typer.BadParameter(f"File {path} does not exist.")
    if not Path(path).is_dir():
        raise typer.BadParameter(f"Path {path} is not a directory.")
