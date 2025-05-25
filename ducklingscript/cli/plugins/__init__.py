from .app import app

from .import_plugin import import_plugin

all_plugin_commands = [
    import_plugin
]

for command in all_plugin_commands:
    app.command()(command)

__all__ = ["app"]
# This module is responsible for initializing the plugins subcommand of the DucklingScript CLI.
