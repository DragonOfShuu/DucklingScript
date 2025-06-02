from .app import app
from .plugin_installer import PluginInstaller


@app.command(name="uninstall", help="Remove a DucklingScript plugin")
def uninstall_plugin(plugin_name: str) -> None:
    """
    Remove a plugin from the DucklingScript environment.

    Args:
        plugin_name (str): The name of the plugin to remove.
    """
    plugin_installer = PluginInstaller.get()
    success = plugin_installer.uninstall_plugin(plugin_name)

    if success:
        print(f"Plugin '{plugin_name}' has been removed successfully.")
    else:
        print(
            f"Failed to remove plugin '{plugin_name}'. It may not exist or the file is in use."
        )
