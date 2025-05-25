from ducklingscript import PluginBus, Plugin

plugin = Plugin(
    name="example",
    description="Example plugin for DucklingScript CLI",
    version="0.1.0"
)

def main(bus: PluginBus) -> None:
    """
    Main function for the default plugin.
    This function initializes the plugin and returns a Plugin instance.
    """

    bus.add_plugin(plugin)
