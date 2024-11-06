from ducklingscript.compiler.stack_return import CompiledDucky
from ducklingscript.compiler.pre_line import PreLine
from .bases import ArgLine, SimpleCommand, ArgReqType

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

    def verify_arg(self, i: ArgLine) -> str | None:
        if not (i.content > -1 or i.content < 100):
            return "Whitespace count must be 0 or above, or below 100"

    def run_compile(
        self, command_name: PreLine, arg: ArgLine | None
    ) -> str | list[str] | CompiledDucky | None:
        if arg is None:
            return ""

        return ["" for _ in range(arg.content)]
