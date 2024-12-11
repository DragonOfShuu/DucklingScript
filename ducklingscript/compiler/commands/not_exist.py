from ducklingscript.compiler.compiled_ducky import CompiledDucky
from ducklingscript.compiler.pre_line import PreLine
from .bases import ArgLine, SimpleCommand, ArgReqType
from ..errors import CompilationError

desc = """
Creates an error if the given variable name DOES exist.
"""


class NotExist(SimpleCommand):
    names = ["NOTEXIST", "NOT_EXIST"]
    tokenize_args = False
    arg_req = ArgReqType.REQUIRED
    description = desc

    def run_compile(
        self, command_name: PreLine, arg: ArgLine
    ) -> str | list[str] | CompiledDucky | None:
        if arg.content not in self.env.var.all_vars:
            return

        raise CompilationError(self.stack, f"'{arg}' does exist.")
