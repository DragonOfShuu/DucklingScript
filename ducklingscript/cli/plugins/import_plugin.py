from typing import Annotated
import typer
import zipfile
from pathlib import Path
import shutil

from ..components.general_component import GeneralComponent

from ..utils.config import Configuration

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

    if not zipfile.is_zipfile(path) and not path.is_dir():
        raise typer.BadParameter(f"File {path} must be a directory or a zip file.")
    
    general_comp = GeneralComponent.get()

    success = actually_import_plugin(path)

    if not success:
        general_comp.print_error(f"Failed to import plugin from {path}")
        return
    
    Configuration.config().plugin_order.append(path.stem)
    Configuration.save()
    general_comp.print(f"Successfully imported plugin from {path}")

def actually_import_plugin(path: Path) -> bool:
    plugin_location = Path(Configuration.config().plugin_location)

    if not plugin_location.exists():
        plugin_location.mkdir(parents=True, exist_ok=True)
    
    if zipfile.is_zipfile(path):
        if not unzip_to_plugin_locations(path, plugin_location):
            return False
        return True
        
    # If it's a directory, copy it to the plugin location
    if path.is_dir():
        if not copy_plugin_to_location(path, plugin_location):
            return False
        return True

    return False

def copy_plugin_to_location(plugin_path: Path, plugin_location: Path):
    general_comp = GeneralComponent.get()

    try:
        shutil.copytree(plugin_path, plugin_location / plugin_path.stem, dirs_exist_ok=True)
    except Exception as e:
        general_comp.print_error(e)
        return False

    return True

def unzip_to_plugin_locations(zip_path: Path, plugin_location: Path):
    """
    Unzips the given zip file to the DucklingScript plugin locations.
    """
    general_comp = GeneralComponent.get()

    if not plugin_location.exists():
        plugin_location.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(plugin_location / zip_path.stem)
    except zipfile.BadZipFile:
        general_comp.print_error(f"Error: {zip_path} is not a valid zip file.")
        return False
    
    return True
