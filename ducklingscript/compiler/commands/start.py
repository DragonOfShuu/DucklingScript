from typing import Any
from .bases.doc_command import ArgReqType

from .bases.simple_command import Line, SimpleCommand
from ducklingscript.compiler.environment import Environment
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from ..errors import (
    InvalidArguments,
    NotAValidCommand,
    CircularStructureError,
    UnexpectedToken,
)

from pathlib import Path

script_extension = ".txt"

desc = '''
Start compiling a different file, and add its
comipiled code to this one, as well as its
ending environment.

START compiles the code, and adds that 
files ending environment to this one.

STARTCODE only compiles the code, and
does not add the file's environment
to this one.

STARTENV only gives the ending environment,
and does not give the compiled code.

Please checkout [the readme section](https://github.com/DragonOfShuu/DucklingScript/#multi-file-projects)
'''

class Start(SimpleCommand):
    names = ["START", "STARTENV", "STARTCODE"]
    arg_req = ArgReqType.REQUIRED
    description = desc

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

        relative_path, stack_wf = self.go_up_directories(relative_path, stack_wf)

        if ".." in relative_path:
            raise UnexpectedToken(
                self.stack,
                "The dot operator can only be used once in between each folder/file name.",
            )

        path = Path(relative_path.replace(".", "/") + script_extension)
        new_file = stack_wf.joinpath(path)
        if not new_file.exists() or not new_file.is_file():
            raise InvalidArguments(
                self.stack, "The path must point to a file, and it must exist."
            )

        self.check_for_circles(new_file)

        return new_file

    def go_up_directories(self, relative_path, stack_wf):
        while relative_path.startswith("."):
            if stack_wf.parent == stack_wf:
                raise UnexpectedToken(
                    self.stack,
                    "Too many dots before the path name. Already at the drive root.",
                )
            stack_wf = stack_wf.parent
            relative_path = relative_path[1:]
        return relative_path, stack_wf

    def check_for_circles(self, similar_import: Path):
        for i in self.stack:
            i: Any
            if i.file == similar_import:
                raise CircularStructureError(
                    self.stack,
                    "A circular structure is being created by a file importing another file that is importing the original file.",
                )

    # def verify_arg(self, i: str) -> str | None:
    def verify_arg(self, arg: Line) -> str | None:
        if arg.content.endswith("."):
            return "The dot operator cannot appear alone at the end of path."

    def run_compile(
        self, commandName: PreLine, arg: Line
    ) -> str | list[str] | CompiledReturn | None:
        from ..compiler import Compiler

        i = self.convert_to_path(arg.content)

        with i.open() as f:
            text = f.read().splitlines()
        commands = Compiler.prepare_for_stack(text)

        run_parallel = commandName.cont_upper() != "STARTCODE"
        with self.stack.add_stack_above(commands, i, run_parallel) as s:
            compiled = s.start_base(False)

        if commandName.cont_upper() in ["START", "STARTCODE"]:
            return compiled
        elif commandName.cont_upper() == "STARTENV":
            return []
