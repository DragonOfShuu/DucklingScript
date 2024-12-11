from __future__ import annotations

import yaml
from dataclasses import asdict
from pathlib import Path

from ..compile_options import CompileOptions
from .base_environment import BaseEnvironment


class ProjectEnvironment(BaseEnvironment):
    """
    The environment for a project. Includes
    configuration data and file sources.
    """
    config_name = "config.yaml"

    def __init__(
        self,
        root_dir: Path | None = None,
        compile_options: CompileOptions | None = None,
    ):
        self.root_dir = root_dir
        self.global_compile_options = (
            CompileOptions() if compile_options is None else compile_options
        )
        self.file_sources: list[Path] = []

    @property
    def global_compile_options(self):
        return self.__global_compile_options

    @global_compile_options.setter
    def global_compile_options(self, value: CompileOptions):
        self.__global_compile_options = value
        self.calculate_options()
        return self.__global_compile_options

    def calculate_options(self):
        self.compile_options = self.global_compile_options

        if self.root_dir is None:
            return
        if not self.__global_compile_options.use_project_config:
            return

        config_file = self.root_dir / self.config_name
        if not config_file.exists():
            return

        with config_file.open() as f:
            new_config = yaml.safe_load(f)

        if new_config is None:
            new_config = {}
        project_options = CompileOptions(**new_config)
        if not project_options.use_project_config:
            return

        compiled_options_dict = asdict(self.__global_compile_options)
        compiled_options_dict.update(asdict(project_options))

        self.compile_options = CompileOptions(**compiled_options_dict)

        with config_file.open("w") as f:
            yaml.dump(
                asdict(self.compile_options),
                f,
            )

    def register_file(self, file_name: Path):
        if file_name in self.file_sources:
            return self.index_of_file(file_name)
        self.file_sources.append(file_name)
        return len(self.file_sources) - 1

    def index_of_file(self, file_name: Path) -> int:
        try:
            return self.file_sources.index(file_name)
        except ValueError:
            return -1

    def append_env(self, x: ProjectEnvironment):
        return

    def update_from_env(self, x: ProjectEnvironment):
        return
