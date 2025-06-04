from enum import Enum
from pathlib import Path
from typing import Annotated

import typer

from ..components.general_component import GeneralComponent
from ..templates.template_manager import TemplateManager, TemplateClass
from .app import app

template_manager = TemplateManager.get()
plugin_templates = {temp.name: temp.name for temp in template_manager.list_templates_by_class(TemplateClass.PLUGINS)}
PluginTemplates = Enum("PluginTemplates", plugin_templates, type=str)


@app.command(name="new", help="Create a new DucklingScript plugin")
def new_plugin(
    name: Annotated[str, typer.Argument(help="Name of the new plugin")],
    path: Annotated[
        Path, typer.Argument(help="Path to the new plugin directory")
    ] = Path("."),
    template: Annotated[PluginTemplates, typer.Option(help="Template to use for the plugin")] = PluginTemplates['default']
):
    path.mkdir(parents=True, exist_ok=True)
    plugin_path = path / name
    plugin_path.mkdir(parents=True, exist_ok=True)

    general_component = GeneralComponent.get()

    template_data = template_manager.get_template(TemplateClass.PLUGINS, template.value)

    if not template_data:
        general_component.print_error(f"No plugin template found for '{template}'.")
        raise typer.Exit(code=1)

    template_path = template_data.directory
    template_manager.copy_template(template_path, plugin_path)

    general_component.print(f"Created new plugin at {plugin_path}")
    general_component.print(f'Run "cd {plugin_path}" to enter the plugin directory.')
