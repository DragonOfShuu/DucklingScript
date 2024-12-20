from .bases.doc_command import ArgReqType
from ..errors import CompilationError
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.compiled_ducky import CompiledDucky
from .bases import ArgLine, SimpleCommand

desc = """
Creates an error if the given variable name DOES NOT exist.
"""


class Exist(SimpleCommand):
    names = ["EXIST"]
    arg_req = ArgReqType.REQUIRED
    description = desc

    def run_compile(
        self, command_name: PreLine, arg: ArgLine
    ) -> str | list[str] | CompiledDucky | None:
        if arg.content in self.env.var.all_vars:
            return

        raise CompilationError(self.stack, f"'{arg}' does not exist.")
