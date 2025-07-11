from __future__ import annotations
from math import inf
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..commands.bases.base_command import BaseCommand
    from quackinter import Command as QuackinterCommand
    from .plugin import Plugin


class PluginBus:
    """
    The plugin bus is a container for plugins.
    It allows for easy management of plugins, including adding, sorting, and
    filtering them. By filtering, I mean that it filters out plugins that are
    not in the given order config.
    """

    def __init__(self, parent: PluginBus | None = None, include_defaults: bool = True):
        from .ducklingscript_plugin import DucklingScriptPlugin

        self.plugins: list["Plugin"] = (
            [DucklingScriptPlugin()] if include_defaults else []
        )
        self._parent: PluginBus | None = parent

    def add_plugin(self, plugin: "Plugin"):
        """
        Add a plugin to the bus. (skrr skrr)
        """
        self.plugins.append(plugin)

    def add_plugins(self, *plugins: "Plugin"):
        """
        Add multiple plugins to the bus. (skrr skrr, now it's a party)
        """
        self.plugins.extend(plugins)

    def mini_bus(self) -> PluginBus:
        """
        Create a child plugin bus.

        This is useful for creating a bus that is a subset of the current bus.
        It will not include the default plugins.

        Ideally this is used in a `with` statement to ensure that the plugins
        added to the mini bus are added to the parent bus when the
        `with` statement is exited.
        """
        return PluginBus(self, include_defaults=False)

    def sort_and_filter_plugins(self, order: list[str]):
        """
        Returns the current plugins sorted by the given order.

        If a plugin's name is not in the order, it will be filtered out.
        """
        plugins_filtered = filter(lambda x: x._name in order, self.plugins)
        plugins_sorted = sorted(
            plugins_filtered,
            key=lambda x: (inf if not x._name else order.index(x._name)),
        )
        self.plugins = plugins_sorted
        return plugins_sorted

    def collect_commands(self) -> list[type["BaseCommand"]]:
        """
        Collect all command accross all currently loaded plugins.
        """
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
        """
        Collect all interpretations across all currently loaded plugins.
        """
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
