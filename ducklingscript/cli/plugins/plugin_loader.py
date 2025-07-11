from typing import Callable, Protocol
from pathlib import Path
import importlib.util
import inspect

from ...compiler.plugins.plugin import Plugin

from ...compiler.plugins import PluginBus
from ..utils.errors import CliPluginError, PluginLoadError, PluginMainMethodMissingError
from ..utils.config import Configuration
import sys


class PluginMainMethod(Protocol):
    def __call__(self) -> Plugin:
        """Main method of the plugin."""
        ...


class PluginLoader:
    """
    PluginLoader is a singleton class that is responsible for loading plugins.
    It gathers all plugins from the specified plugin directory, imports them,
    and initializes them. It also provides a method to access the PluginBus
    that contains all loaded plugins.
    """

    _instance = None

    def __init__(self):
        self.bus: PluginBus | None = None

    @staticmethod
    def get():
        if PluginLoader._instance is None:
            PluginLoader._instance = PluginLoader()
        return PluginLoader._instance

    def load_plugins(self, output: Callable[[str], None]):
        """
        Load plugins from the configured plugin location,
        initialize them, and return the PluginBus with all of the plugins.
        """
        plugins_path = Path(Configuration.config().plugin_location)
        if not plugins_path.is_dir():
            raise ValueError(
                f"Plugins path '{plugins_path}' does not exist or is not a directory."
            )

        main_methods = self.gather_main_methods(plugins_path, output)
        bus = self.initialize_plugins(main_methods)
        bus.sort_and_filter_plugins(Configuration.config().plugin_order)
        self.bus = bus
        return bus

    def initialize_plugins(self, main_methods: dict[str, PluginMainMethod]):
        """
        Create a PluginBus that contains all initialized plugins.

        :param main_methods: A dictionary mapping plugin names to their main methods.
        Main methods should be callable and return an instance of Plugin.

        :return: A PluginBus instance containing all loaded plugins.

        :raises PluginLoadError: If any plugin fails to load.
        """
        plugin_bus = PluginBus()
        for plugin_name, main in main_methods.items():
            try:
                with plugin_bus.mini_bus() as mini:
                    returned = main()
                    if isinstance(returned, Plugin):
                        returned._name = plugin_name
                        mini.add_plugin(returned)
            except Exception as e:
                raise PluginLoadError(
                    plugin_name, f"Failed to load plugin due to error: {str(e)}"
                ) from e

        return plugin_bus

    def gather_main_methods(self, plugins_path: Path, output: Callable[[str], None]):
        """
        Gather all main methods from plugins in the specified directory.

        :param plugins_path: Path to the directory containing plugins.
        :param output: A callable to output messages, typically for logging or user feedback.
        :return: A dictionary mapping plugin names to their main methods.
        """
        main_methods: dict[str, PluginMainMethod] = {}
        for plugin_path in plugins_path.iterdir():
            try:
                plugin_main = self.import_plugin(plugin_path)
                if plugin_main is None:
                    output(
                        f"Plugin '{plugin_path.name}' does not have a valid main method."
                    )
                    continue
                main_methods[plugin_path.name] = plugin_main
            except CliPluginError as e:
                output(f"Plugin '{plugin_path.name}' failed to load: {str(e)}")

        return main_methods

    def import_plugin(self, plugin_path: Path) -> PluginMainMethod | None:
        """
        Import the plugin from the specified path.

        Returns the main method of the plugin if it exists and is callable.

        :param plugin_path: Path to the plugin directory.
        :return: The main method of the plugin if it exists and is callable, otherwise None.
        :raises PluginMainMethodMissingError: If the plugin does not have a main method.
        :raises PluginLoadError: If the plugin cannot be loaded due to import errors.
        """
        if not plugin_path.is_dir():
            return

        main_file = plugin_path / "__init__.py"

        if not main_file.is_file():
            raise PluginMainMethodMissingError(plugin_path.name)

        plugin_name = plugin_path.name
        module = self._attempt_import(plugin_name, main_file)
        main_method = self._verify_main_method(module.main, plugin_name)

        return main_method

    def _attempt_import(self, plugin_name: str, plugin_dir: Path):
        """
        Attempt to import the plugin module from the specified directory.

        :param plugin_name: The name of the plugin.
        :param plugin_dir: The directory where the plugin is located.
        :return: The imported module.
        :raises PluginLoadError: If the plugin cannot be loaded due to import errors.
        """
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_dir)
        if spec is None or spec.loader is None:
            raise PluginLoadError(plugin_name, "Failed to load plugin spec")

        module = importlib.util.module_from_spec(spec)
        sys.modules[plugin_name] = module
        spec.loader.exec_module(module)

        if not hasattr(module, "main"):
            raise PluginMainMethodMissingError(plugin_name)

        return module

    def _verify_main_method(self, method: Callable, plugin_name: str):
        """
        Verify that the main method of the plugin is callable,
        and has the correct signature (the correct number of arguments).

        :param method: The main method of the plugin.
        :param plugin_name: The name of the plugin.
        :return: The main method if it is valid.
        :raises PluginLoadError: If the main method is not callable or does not have the
        correct signature.
        """
        if not callable(method):
            raise PluginLoadError(plugin_name, "Plugin main method is not callable")

        argspec = inspect.getfullargspec(method)
        defaults = argspec.defaults
        args = argspec.args

        if len(args) == 0:
            return method

        if len(args) > 0 and defaults and (len(args) - len(defaults) == 0):
            return method

        raise PluginLoadError(
            plugin_name, "Main method must have 0 or default arguments only"
        )
