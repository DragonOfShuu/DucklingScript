from __future__ import annotations
from math import inf
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..commands.bases.base_command import BaseCommand
    from quackinter import Command as QuackinterCommand
    from .plugin import Plugin


class PluginBus:
    def __init__(self, parent: PluginBus | None = None, include_defaults: bool = True):
        from .ducklingscript_plugin import DucklingScriptPlugin
        self.plugins: list["Plugin"] = (
            [DucklingScriptPlugin()] if include_defaults else []
        )
        self._parent: PluginBus | None = parent

    def add_plugin(self, plugin: "Plugin"):
        self.plugins.append(plugin)

    def add_plugins(self, *plugins: "Plugin"):
        self.plugins.extend(plugins)

    def mini_bus(self) -> PluginBus:
        return PluginBus(self, include_defaults=False)

    def sort_and_filter_plugins(self, order: list[str]):
        plugins_filtered = filter(lambda x: x._name in order, self.plugins)
        plugins_sorted = sorted(
            plugins_filtered,
            key=lambda x: (inf if not x._name else order.index(x._name)),
        )
        self.plugins = plugins_sorted
        return plugins_sorted

    def collect_commands(self) -> list[type["BaseCommand"]]:
        # Use a simple cache that is invalidated if self.plugins changes
        if hasattr(self, "_commands_cache") and getattr(
            self, "_plugins_snapshot", None
        ) == list(self.plugins):
            return self._commands_cache

        commands: list[type["BaseCommand"]] = []
        for plugin in self.plugins:
            commands.extend(plugin.get_commands())
        self._commands_cache = commands
        self._plugins_snapshot = list(self.plugins)
        return commands

    def collect_interpretations(self) -> list[type["QuackinterCommand"]]:
        if hasattr(self, "_interpretations_cache") and getattr(
            self, "_plugins_snapshot", None
        ) == list(self.plugins):
            return self._interpretations_cache

        interpretations: list[type["QuackinterCommand"]] = []
        for plugin in self.plugins:
            interpretations.extend(plugin.get_interpretations())
        self._interpretations_cache = interpretations
        self._plugins_snapshot = list(self.plugins)
        return interpretations

    def as_list(self) -> list["Plugin"]:
        return self.plugins

    def __iter__(self):
        return iter(self.plugins)

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        if exc_type is not None:
            return

        if self._parent is None:
            raise RuntimeError("Cannot exit a plugin bus that has no parent.")

        self._parent.add_plugins(*self.plugins)
