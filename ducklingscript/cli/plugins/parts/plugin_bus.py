from __future__ import annotations

from .plugin import Plugin


class PluginBus:
    def __init__(self, parent: PluginBus | None = None):
        self.plugins: list[Plugin] = []
        self._parent: PluginBus | None = parent

    def add_plugin(self, plugin: Plugin):
        self.plugins.append(plugin)
    
    def add_plugins(self, *plugins: Plugin):
        self.plugins.extend(plugins)

    def mini_bus(self) -> PluginBus:
        return PluginBus(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: object | None) -> None:
        if exc_type is not None:
            return

        if self._parent is None:
            raise RuntimeError("Cannot exit a plugin bus that has no parent.")
        
        self._parent.add_plugins(*self.plugins)
        