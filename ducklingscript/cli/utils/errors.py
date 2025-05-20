
class CLIError(Exception):
    """Base class for all CLI-related errors."""
    pass

class PluginError(CLIError):
    """Base class for all plugin-related errors."""
    pass

class PluginLoadError(PluginError):
    """Raised when a plugin fails to load."""
    def __init__(self, plugin_name: str, message: str) -> None:
        super().__init__(f"Failed to load plugin '{plugin_name}': {message}")
        self.plugin_name = plugin_name
        self.message = message

class PluginMainMethodMissingError(PluginError):
    """Raised when a plugin's main method is missing."""
    def __init__(self, plugin_name: str) -> None:
        super().__init__(f"Plugin '{plugin_name}' does not have a main method.")
        self.plugin_name = plugin_name
