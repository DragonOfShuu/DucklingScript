from pathlib import Path

import importlib.util

from .plugin_bus import PluginBus

from ...utils.config import Configuration

class PluginSystem:
    plugins = []

    @classmethod
    def load_plugins(cls):
        plugins_path = Path(Configuration.config().plugin_location)
        if not plugins_path.is_dir():
            raise ValueError(f"Plugins path '{plugins_path}' does not exist or is not a directory.")

        main_methods = []
        plugin_bus = PluginBus()
        for plugin_dir in plugins_path.iterdir():
            if not plugin_dir.is_dir():
                continue

            plugin_path = plugins_path / plugin_dir
            main_file = plugin_path / "main.py"
            if not main_file.is_file():
                continue

            module_name = f"plugin_{plugin_dir}"
            spec = importlib.util.spec_from_file_location(module_name, main_file)
            if spec is None:
                continue

            module = importlib.util.module_from_spec(spec)
            # try:
            #     spec.loader.exec_module(module)
            # except Exception as e:
            #     print(f"Error loading plugin '{plugin_dir}': {e}")
            #     continue

            if not hasattr(module, "main"):
                continue

            main_methods.append(module.main)
            cls.plugins.append(module)

        for main in main_methods:
            try:
                main(plugin_bus)
            except Exception as e:
                continue
    
    @classmethod
    def attempt_import(cls):
        pass