

from .plugin import Plugin
from ..commands import command_palette

class DucklingScriptPlugin(Plugin):
    def __init__(self):
        super().__init__("DucklingScript", "The Main Plugin for DucklingScript")

        self.add_commands(*command_palette)
