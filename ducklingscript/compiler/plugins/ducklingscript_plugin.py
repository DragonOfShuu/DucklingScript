from .plugin import Plugin
from ..commands import command_palette


class DucklingScriptPlugin(Plugin):
    """
    The main DucklingScript plugin.
    This plugin is responsible for integrating DucklingScript commands into the compiler.
    """

    def __init__(self):
        super().__init__("DucklingScript", "The Main Plugin for DucklingScript")

        self.add_commands(*command_palette)
        self._name = "ducklingscript"
