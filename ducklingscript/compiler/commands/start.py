from typing import Any

from ducklingscript.compiler.tokenization import token_return_types
from .bases.simple_command import SimpleCommand
from ducklingscript.compiler.environment import Environment
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import StackReturnType, CompiledReturn
from ..errors import (
    InvalidArguments,
    CompilationError,
    NotAValidCommand,
    CircularStructureError,
)

from pathlib import Path

script_extension = ".txt"


class Start(SimpleCommand):
    names = ["START", "STARTENV", "STARTCODE"]

    def __init__(self, env: Environment, stack: Any):
        if stack.file is None:
            raise NotAValidCommand(
                stack, "The START command cannot be used outside of a file."
            )

        super().__init__(env, stack)

    def convert_to_path(self, relative_path: str) -> Path:
        # Folder the stack is inside
        if self.stack.file is None:
            raise TypeError("Stack should not be None here. This should be impossible")
        stack_wf: Path = self.stack.file.parent

        path = Path(relative_path.replace(".", "/") + script_extension)
        new_file = stack_wf.joinpath(path)
        if not new_file.exists() or not new_file.is_file():
            raise InvalidArguments(
                self.stack, "The path must point to a file, and it must exist."
            )

        return new_file

    def check_for_circles(self, similar_import: Path):
        for i in self.stack:
            i: Any
            if i.file == similar_import:
                raise CircularStructureError(
                    self.stack,
                    "A circular structure is being created by a file importing another file that is importing the original file.",
                )

    def verify_arg(self, i: str) -> str | None:
        if i.startswith(".") or i.endswith("."):
            return "The dot operator cannot be at the beginning or end of path."
        try:
            arg_path = self.convert_to_path(i)
        except CompilationError as e:
            return e.args[0]

        self.check_for_circles(arg_path)

    def run_compile(
        self, commandName: PreLine, all_args: list[str]
    ) -> list[str] | CompiledReturn | None:
        all_files = [self.convert_to_path(i) for i in all_args]
        from ..compiler import Compiler

        returnable: list[str] = []
        for i in all_files:
            with i.open() as f:
                text = f.read().splitlines()
            commands = Compiler.prepare_for_stack(text)

            run_parallel = commandName.cont_upper() != "STARTCODE"
            with self.stack.add_stack_above(commands, i, run_parallel) as s:
                returnable.extend(s.start_base(False))

        if commandName.cont_upper() in ["START", "STARTCODE"]:
            return returnable
        elif commandName.cont_upper() == "STARTENV":
            return []
