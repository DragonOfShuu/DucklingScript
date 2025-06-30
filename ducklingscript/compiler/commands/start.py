from ..environments.env_extend_type import EnvExtendType
from .bases.doc_command import ArgReqType
from .utility.file_path import convert_to_path
from .bases.simple_command import ArgLine, SimpleCommand
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.compiled_ducky import CompiledDucky
from ..errors import (
    NotAValidCommandError,
)

desc = """
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
"""


class Start(SimpleCommand):
    names = ["START", "STARTENV", "STARTCODE"]
    arg_req = ArgReqType.REQUIRED
    description = desc

    def verify_arg(self, arg: ArgLine) -> str | None:
        if arg.content.endswith("."):
            return "The dot operator cannot appear alone at the end of path."

    def run_compile(self, command_name: PreLine, arg: ArgLine) -> CompiledDucky | None:
        from ..compiler import DucklingCompiler

        if self.stack.file is None:
            raise NotAValidCommandError(
                self.stack, "The START command cannot be used outside of a file."
            )

        file_path = convert_to_path(self.stack_pile, self.stack.file, arg.content)

        with file_path.open() as f:
            text = f.read().splitlines()

        file_index = self.env.proj.register_file(file_path)

        commands = DucklingCompiler._prepare_for_stack(text, file_index)

        run_parallel = command_name.content_as_upper() != "STARTCODE"
        with self.stack_pile.add_stack_above(
            commands,
            file_path,
            EnvExtendType.PARALLEL if run_parallel else EnvExtendType.NORMAL,
        ) as s:
            compiled = s.run()

        if command_name.content_as_upper() in ["START", "STARTCODE"]:
            return compiled
        elif command_name.content_as_upper() == "STARTENV":
            return CompiledDucky()
