from dataclasses import dataclass, asdict
from pathlib import Path
import yaml

@dataclass
class Config:
    flipper_commands: bool = True
    supress_command_not_exist: bool = False

    def to_dict(self):
        return asdict(self)


class Configuration:
    config: Config|None = None
    rsrc_path: Path = Path.home() / ".duckling"
    config_file = rsrc_path / "config.yaml"

    @classmethod
    def load(cls):
        if not cls.config_file.exists():
            cls.save()
        with cls.config_file.open() as f:
            return yaml.safe_load(f)

    @classmethod
    def save(cls, x: Config|None = None):
        if x is None:
            x = Config()
        with cls.config_file.open('w') as f:
            yaml.dump(x.to_dict(), f)