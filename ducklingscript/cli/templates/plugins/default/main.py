from ducklingscript import Plugin

plugin = Plugin(
    display_name="example",
    description="Example plugin for DucklingScript CLI",
    version="0.1.0"
)

def main() -> Plugin:
    """
    Main function for the default plugin.
    This function initializes the plugin and returns a Plugin instance.
    """

    return plugin
