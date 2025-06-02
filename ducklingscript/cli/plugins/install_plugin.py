from typing import Annotated
import typer
import zipfile
from pathlib import Path
from rich import print

from .plugin_installer import PluginInstaller

from ..components.general_component import GeneralComponent

from .app import app


@app.command(name="install", help="Import a DucklingScript plugin from a directory")
def install_plugin(
    path: Annotated[Path, typer.Argument(help="Path to the plugin file")],
):
    """
    Import a DucklingScript plugin from a directory.
    """
    # Check if the file exists
    if not Path(path).exists():
        raise typer.BadParameter(f"File {path} does not exist.")

    if not zipfile.is_zipfile(path) and not path.is_dir():
        raise typer.BadParameter(f"File {path} must be a directory or a zip file.")

    general_comp = GeneralComponent.get()

    plugins = PluginInstaller.get().install_plugin(path, print)

    if not plugins:
        general_comp.print_error(f"Failed to import plugin from {path}")
        return

    general_comp.print(f"Successfully imported plugin from {path}")
