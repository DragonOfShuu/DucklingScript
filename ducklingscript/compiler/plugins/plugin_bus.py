from __future__ import annotations

from ..commands.bases.base_command import BaseCommand

from .ducklingscript_plugin import DucklingScriptPlugin

from .plugin import Plugin


class PluginBus:
    def __init__(self, parent: PluginBus | None = None, include_defaults: bool = True):
        self.plugins: list[Plugin] = [DucklingScriptPlugin()] if include_defaults else []
        self._parent: PluginBus | None = parent

    def add_plugin(self, plugin: Plugin):
        self.plugins.append(plugin)
    
    def add_plugins(self, *plugins: Plugin):
        self.plugins.extend(plugins)

    def mini_bus(self) -> PluginBus:
        return PluginBus(self, include_defaults=False)

    def sort_and_filter_plugins(self, order: list[str]):
        plugins_filtered = filter(lambda x: x.name in order, self.plugins)
        plugins_sorted = sorted(plugins_filtered, key=lambda x: order.index(x.name))
        self.plugins = plugins_sorted
        return plugins_sorted

    def collect_commands(self) -> list[type[BaseCommand]]:
        # Use a simple cache that is invalidated if self.plugins changes
        if hasattr(self, '_commands_cache') and getattr(self, '_plugins_snapshot', None) == list(self.plugins):
            return self._commands_cache
        
        commands: list[type[BaseCommand]] = []
        for plugin in self.plugins:
            commands.extend(plugin.get_commands())
        self._commands_cache = commands
        self._plugins_snapshot = list(self.plugins)
        return commands

    def as_list(self) -> list[Plugin]:
        return self.plugins

    def __iter__(self):
        return iter(self.plugins)

    def __enter__(self):
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: object | None) -> None:
        if exc_type is not None:
            return

        if self._parent is None:
            raise RuntimeError("Cannot exit a plugin bus that has no parent.")
        
        self._parent.add_plugins(*self.plugins)
        