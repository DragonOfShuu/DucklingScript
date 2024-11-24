from dataclasses import dataclass
from pathlib import Path

from .sourcemapping import SourceMap
from .environments import VariableEnvironment, ProjectEnvironment, Environment
from .compiled_ducky import CompiledDucky, StdOutData
from .pre_line import PreLine
from .stack import Stack
from .compile_options import CompileOptions
from .tab_parse import parse_document
from .errors import WarningsObject
from .commands import command_palette


@dataclass
class Compiled:
    output: list[str]
    compiled: CompiledDucky
    warnings: WarningsObject
    env: Environment
    std_out: list[StdOutData]
    sourcemap: SourceMap | None


class DucklingCompiler:
    def __init__(self, options: CompileOptions | None = None):
        self.compile_options = options

    @staticmethod
    def prepare_for_stack(
        lines: list, file_index: int = 0, skip_indentation: bool = False
    ):
        if not skip_indentation:
            return parse_document(PreLine.convert_to(lines, file_index))
        else:
            return PreLine.convert_to_recur(lines, file_index)

    def compile_file(
        self, file: str | Path, variable_environment: VariableEnvironment | None = None
    ):
        """
        Compile the given file.
        """
        file_path = Path(file)
        if not file_path.exists():
            raise FileNotFoundError(f"The file {file} does not exist.")
        if not file_path.is_absolute():
            file_path = file_path.absolute()
        with open(file_path) as f:
            text = f.read()

        proj_env = ProjectEnvironment(
            root_dir=file_path.parent, compile_options=self.compile_options
        )

        return self.compile(
            text, file_path, proj_env=proj_env, var_env=variable_environment
        )

    def compile(
        self,
        text: str | list,
        file: Path | str | None = None,
        skip_indentation: bool = False,
        proj_env: ProjectEnvironment | None = None,
        var_env: VariableEnvironment | None = None,
    ):
        """
        Compile the given text.
        """
        if isinstance(text, str):
            lines = text.split("\n")
        else:
            lines = text

        if isinstance(file, str):
            file = Path(file)

        file_index = -1
        if proj_env and file:
            file_index = proj_env.register_file(file)

        parsed = self.prepare_for_stack(lines, file_index, skip_indentation)

        env = Environment(var_env, proj_env)
        base_stack = Stack(
            parsed, file, compile_options=env.proj.compile_options, env=env
        )
        env.stack = base_stack

        ducky_code = base_stack.start_base()

        sourcemap = None
        if proj_env and self.compile_options and self.compile_options.create_sourcemap:
            sourcemap = SourceMap.create_sourcemap(ducky_code, proj_env.file_sources)

        return Compiled(
            ducky_code.get_ducky(),
            ducky_code,
            base_stack.warnings,
            base_stack.env,
            base_stack.std_out,
            sourcemap,
        )

    @staticmethod
    def get_docs(command_name: str):
        command = DucklingCompiler.get_command(command_name)

        if command is None:
            return None

        return command.get_doc()

    @staticmethod
    def get_command(command_name: str):
        command_name = command_name.strip().upper()

        for i in command_palette:
            if command_name in i.names:
                return i
        else:
            return None
