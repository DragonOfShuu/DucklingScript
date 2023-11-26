from ducklingscript.compiler.stack_return import CompiledReturn
from ducklingscript.compiler.pre_line import PreLine
from .bases import Line, SimpleCommand, ArgReqType
from ..errors import GeneralError

desc = """
Creates an error if the given variable name DOES exist.
"""


class NotExist(SimpleCommand):
    names = ["NOTEXIST", "NOT_EXIST"]
    tokenize_args = False
    arg_req = ArgReqType.REQUIRED
    description = desc

    def run_compile(
        self, commandName: PreLine, arg: Line
    ) -> str | list[str] | CompiledReturn | None:
        if arg.content not in self.env.all_vars:
            return

        raise GeneralError(self.stack, f"'{arg}' does exist.")
