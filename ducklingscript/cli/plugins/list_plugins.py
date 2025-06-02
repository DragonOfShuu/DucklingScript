from ..utils.config import Configuration
from .plugin_loader import PluginLoader
from rich import print
from .app import app


@app.command(name="list", help="List all DucklingScript plugins")
def list_plugins():
    """
    List all available plugins.
    """
    loader = PluginLoader.get()
    plugins = loader.load_plugins(print)
    if not plugins:
        print("No plugins found.")
        return

    # Print the list of available plugins
    print("[bold blue]Available plugins:[/bold blue]")
    for plugin in plugins:
        print(f"- [i]{plugin._name}[/i]")
        print(f"--> [i]{plugin.description}[/i]")

    # Print the plugin order
    print("\n[bold green]Plugin Order:[/bold green]")
    plugin_order = Configuration.config().plugin_order

    if not plugin_order:
        print("No plugins in order.")
        return

    for plugin in plugin_order:
        print(f"- [i]{plugin}[/i]")
