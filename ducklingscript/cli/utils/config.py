from dataclasses import dataclass, field, fields
from pathlib import Path
from ducklingscript import CompileOptions
import yaml

from .config_compat import verify_compat


default_rsrc_path = Path.home() / ".duckling"
default_config_file = default_rsrc_path / "config.yaml"

class Null:
    pass

@dataclass
class Config(CompileOptions):
    plugin_location: Path = Path.home() / ".duckling" / "plugins"
    
    def get_compile_options(self) -> CompileOptions:
        return super()

class Configuration:
    _config: Config | None = None
    rsrc_path: Path = default_rsrc_path
    config_file = default_config_file

    __load_attempted: bool = False

    @classmethod
    def load(cls):
        cls.__load_attempted = True
        if not cls.config_file.exists():
            cls.save()
            return

        with cls.config_file.open() as f:
            new_config = yaml.safe_load(f)

        if new_config is None:
            cls.save()
            return

        new_config = verify_compat(new_config)
        cls._config = Config(**new_config)
        cls.save()

    @classmethod
    def config(cls) -> Config:
        if cls._config is None:
            cls.load()
        return cls._config  # type: ignore

    @classmethod
    def save(cls):
        if not cls.__load_attempted:
            cls.load()
            return

        if cls._config is None:
            cls._config = Config()

        cls.create_dir()
        with cls.config_file.open("w") as f:
            yaml.dump(cls.config().to_dict(), f)

    @classmethod
    def create_dir(cls):
        if not cls.rsrc_path.exists():
            cls.rsrc_path.mkdir()
