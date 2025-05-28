from pathlib import Path
from typing import Annotated

import typer

from ..components.general_component import GeneralComponent
from ..templates.template_manager import TemplateManager, TemplateClass
from .app import app

@app.command(name="new", help="Create a new DucklingScript plugin")
def new_plugin(name: Annotated[str, typer.Argument(help="Name of the new plugin")], path: Annotated[Path, typer.Argument(help="Path to the new plugin directory")] = Path(".")):
    path.mkdir(parents=True, exist_ok=True)
    plugin_path = path / name
    plugin_path.mkdir(parents=True, exist_ok=True)

    template_manager = TemplateManager.get()
    general_component = GeneralComponent.get()

    template = template_manager.get_template(TemplateClass.PLUGINS, "default")
    if not template:
        general_component.print_error("No default plugin template found.")
        raise typer.Exit(code=1)

    template_path = template.directory
    template_manager.copy_template(template_path, plugin_path)

    general_component.print(f"Created new plugin at {plugin_path}")
    general_component.print(f"Run \"cd {plugin_path}\" to enter the plugin directory.")
