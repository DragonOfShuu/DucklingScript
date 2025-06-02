from .app import app

from .install_plugin import install_plugin
from .uninstall_plugin import uninstall_plugin
from .new_plugin import new_plugin
from .list_plugins import list_plugins

all_plugin_commands = [
    install_plugin,
    uninstall_plugin,
    new_plugin,
    list_plugins,
]
