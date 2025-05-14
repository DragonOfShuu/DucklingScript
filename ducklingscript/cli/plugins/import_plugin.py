import typer
from pathlib import Path


def import_plugin(
    path: str = typer.Argument(Path, help="Path to the plugin file"),
):
    """
    Import a DucklingScript plugin from a directory.
    """
    # Check if the file exists
    if not Path(path).exists():
        raise typer.BadParameter(f"File {path} does not exist.")
    if not Path(path).is_dir():
        raise typer.BadParameter(f"Path {path} is not a directory.")
