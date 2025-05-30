from .app import app

from .install_plugin import install_plugin
from .new_plugin import new_plugin

all_plugin_commands = [
    install_plugin,
    new_plugin,
]
