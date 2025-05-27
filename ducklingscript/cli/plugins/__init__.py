from .app import app

from .import_plugin import import_plugin
from .new_plugin import new_plugin

all_plugin_commands = [
    import_plugin,
    new_plugin,
]
