from dataclasses import dataclass
from pathlib import Path

from .environments import VariableEnvironment, ProjectEnvironment, Environment
from .stack_return import StdOutData
from .pre_line import PreLine
from .stack import Stack
from .compile_options import CompileOptions
from .tab_parse import parse_document
from .errors import WarningsObject
from .environments.environment import Environment
from .commands import command_palette


@dataclass
class Compiled:
    output: list[str]
    warnings: WarningsObject
    env: Environment
    std_out: list[StdOutData]


class Compiler:
    def __init__(self, options: CompileOptions | None = None):
        self.compile_options = options

    @staticmethod
    def prepare_for_stack(lines: list, skip_indentation: bool = False):
        if not skip_indentation:
            return parse_document(PreLine.convert_to(lines))
        else:
            return PreLine.convert_to_recur(lines)

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

        parsed = self.prepare_for_stack(lines, skip_indentation)

        env = Environment(var_env, proj_env)
        base_stack = Stack(
            parsed, file, compile_options=env.proj.compile_options, env=env
        )
        env.stack = base_stack

        returnable = base_stack.start_base()

        return Compiled(
            returnable, base_stack.warnings, base_stack.env, base_stack.std_out
        )

    @staticmethod
    def get_docs(commandName: str):
        command = Compiler.get_command(commandName)

        if command is None:
            return None

        return command.get_doc()

    @staticmethod
    def get_command(commandName: str):
        commandName = commandName.strip().upper()

        for i in command_palette:
            if commandName in i.names:
                return i
        else:
            return None
