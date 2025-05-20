from typing import Callable, Protocol
from pathlib import Path
import importlib.util
import inspect

from .plugin import Plugin

from ...utils.errors import PluginError, PluginLoadError, PluginMainMethodMissingError
from .plugin_bus import PluginBus
from ...utils.config import Configuration


class PluginMainMethod(Protocol):
    def __call__(self, bus: PluginBus) -> None:
        """Main method of the plugin."""
        pass

class PluginSystem:
    _instance = None

    def __init__(self):
        self.plugins = []

    @staticmethod
    def get():
        if PluginSystem._instance is None:
            PluginSystem._instance = PluginSystem()
        return PluginSystem._instance

    def load_plugins(self, output: Callable[[str], None]):
        plugins_path = Path(Configuration.config().plugin_location)
        if not plugins_path.is_dir():
            raise ValueError(f"Plugins path '{plugins_path}' does not exist or is not a directory.")

        main_methods = self.gather_main_methods(plugins_path, output)
        bus = self.initialize_plugins(main_methods)
        plugins = self.sort_and_filter_plugins(bus.plugins, Configuration.config().plugin_order)
        self.plugins = plugins
        return plugins

    def initialize_plugins(self, main_methods: dict[str, PluginMainMethod]):
        plugin_bus = PluginBus()
        for plugin_name, main in main_methods.items():
            try:
                with plugin_bus.mini_bus() as mini:
                    main(mini)
            except Exception as e:
                raise PluginLoadError(plugin_name, f"Failed to load plugin due to error: {str(e)}") from e

        return plugin_bus

    def sort_and_filter_plugins(self, plugins: list[Plugin], order: list[str]):
        plugins_filtered = filter(lambda x: x.name in order, plugins)
        plugins_sorted = sorted(plugins_filtered, key=lambda x: order.index(x.name))
        return plugins_sorted

    def gather_main_methods(self, plugins_path: Path, output: Callable[[str], None]):
        main_methods: dict[str, PluginMainMethod] = {}
        for plugin_path in plugins_path.iterdir():
            try:
                plugin_main = self.import_plugin(plugin_path)
                if plugin_main is None:
                    continue
                main_methods[plugin_path.name] = plugin_main
            except PluginError as e:
                output(f"Plugin '{plugin_path.name}' failed to load: {str(e)}")

        return main_methods

    def import_plugin(self, plugin_path: Path) -> PluginMainMethod | None:
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
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_dir)
        if spec is None:
            raise PluginLoadError(plugin_name, "Failed to load plugin spec")

        module = importlib.util.module_from_spec(spec)

        if not hasattr(module, "main"):
            raise PluginMainMethodMissingError(plugin_name)

        return module

    def _verify_main_method(self, method: Callable, plugin_name: str):
        if not callable(method):
            raise PluginLoadError(plugin_name, "Plugin main method is not callable")

        argspec = inspect.getfullargspec(method)
        defaults = argspec.defaults
        args = argspec.args

        if len(args) == 1:
            return method

        if len(args) < 1:
            raise PluginLoadError(plugin_name, "main method has 0 arguments. (Must have plugin bus arg)")

        if len(args) > 1 and defaults and (len(args) - len(defaults) == 1):
            return method

        raise PluginLoadError(plugin_name, "Main method must have exactly one argument of type 'PluginBus'.")
