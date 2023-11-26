from ducklingscript.compiler.stack_return import CompiledReturn
from ducklingscript.compiler.pre_line import PreLine
from .bases import Line, SimpleCommand, ArgReqType

desc = """
Add whitespaces that will appear in
compiled form. 

If no arguments are given, then 
there will be one whitespace.
The argument is an integer, for 
the amount of whitespaces there
should be.
"""


class Whitespace(SimpleCommand):
    names = ["WHITESPACE"]
    tokenize_args = True
    arg_type = int
    arg_req = ArgReqType.ALLOWED
    description = desc

    def verify_arg(self, i: int) -> str | None:
        if not (i > -1 or i < 100):
            return "Whitespace count must be 0 or above, or below 100"

    def run_compile(
        self, commandName: PreLine, arg: Line | None
    ) -> str | list[str] | CompiledReturn | None:
        if arg is None:
            return ""

        return ["" for _ in range(arg.content)]
