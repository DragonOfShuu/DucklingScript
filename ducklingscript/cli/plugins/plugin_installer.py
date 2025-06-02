from typing import Callable, Literal
from pathlib import Path
import zipfile
import shutil

from ..components.general_component import GeneralComponent
from ...compiler.plugins.plugin import Plugin
from .plugin_loader import PluginLoader
from ..utils.config import Configuration

class PluginInstaller:
    _instance = None

    def __init__(self):
        self.general_component = GeneralComponent.get()

    @staticmethod
    def get():
        if PluginInstaller._instance is None:
            PluginInstaller._instance = PluginInstaller()
        return PluginInstaller._instance
    
    def install_plugin(self, path: Path, output: Callable[[str], None] = lambda x: None) -> Literal[False] | Plugin:
        plugin_location = Path(Configuration.config().plugin_location)

        if not plugin_location.exists():
            plugin_location.mkdir(parents=True, exist_ok=True)
        
        success = self._attempt_install(path, plugin_location)
        if not success:
            return False

        installed_location = plugin_location / path.stem

        success = False
        try:
            loaded_plugin = self._attempt_get_plugin(installed_location)
            if loaded_plugin:
                Configuration.config().plugin_order.append(path.stem)
                Configuration.save()
                return loaded_plugin
        except Exception as e:
            output(f"Exception {e.__class__.__name__}: {e}")

        output(f"Failed to load plugin from {path}. It may not have a valid main method or is not a DucklingScript plugin.")
        self.uninstall_plugin(path.stem)
        return False

    def uninstall_plugin(self, plugin_name: str) -> bool:
        plugin_location = Path(Configuration.config().plugin_location) / plugin_name

        if not plugin_location.exists():
            return False

        shutil.rmtree(plugin_location, ignore_errors=True)

        try:
            Configuration.config().plugin_order.remove(plugin_name)
            Configuration.save()
        except ValueError:
            pass

        return True

    def _attempt_install(self, path: Path, plugin_location: Path) -> bool:
        if zipfile.is_zipfile(path):
            if not self.unzip_to_plugin_locations(path, plugin_location):
                return False
            return True
            
        # If it's a directory, copy it to the plugin location
        if path.is_dir():
            if not self.copy_plugin_to_location(path, plugin_location):
                return False
            return True

        return False

    def _attempt_get_plugin(self, path: Path) -> Literal[False] | Plugin:
        loader = PluginLoader.get()
        main_method = loader.import_plugin(path)
        if not main_method:
            # self.general_component.print_error(f"Plugin '{path.name}' does not have a valid main method.")
            return False
        loader.initialize_plugins({path.stem: main_method})

        return main_method()

    def copy_plugin_to_location(self, plugin_path: Path, plugin_location: Path):
        general_comp = GeneralComponent.get()

        try:
            shutil.copytree(plugin_path, plugin_location / plugin_path.stem, dirs_exist_ok=True)
        except Exception as e:
            general_comp.print_error(e)
            return False

        return True

    def unzip_to_plugin_locations(self, zip_path: Path, plugin_location: Path):
        """
        Unzips the given zip file to the DucklingScript plugin locations.
        """
        general_comp = GeneralComponent.get()

        if not plugin_location.exists():
            plugin_location.mkdir(parents=True, exist_ok=True)

        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(plugin_location / zip_path.stem)
        except zipfile.BadZipFile:
            general_comp.print_error(f"Error: {zip_path} is not a valid zip file.")
            return False
        
        return True