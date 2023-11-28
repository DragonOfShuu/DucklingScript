from pathlib import Path
from ducklingscript import CompileOptions
import yaml

Config = CompileOptions


class Configuration:
    _config: Config | None = None
    rsrc_path: Path = Path.home() / ".duckling"
    config_file = rsrc_path / "config.yaml"

    __load_attempted: bool = False

    @classmethod
    def load(cls):
        cls.__load_attempted = True
        if not cls.config_file.exists():
            cls.save()
            return

        with cls.config_file.open() as f:
            new_config = yaml.safe_load(f)
        cls._config = Config(**new_config)

    @classmethod
    @property
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
            yaml.dump(cls.config.to_dict(), f)

    @classmethod
    def create_dir(cls):
        if not cls.rsrc_path.exists():
            cls.rsrc_path.mkdir()
