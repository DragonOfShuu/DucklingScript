from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from .bases import Line, SimpleCommand, ArgReqType


class Whitespace(SimpleCommand):
    names = ["WHITESPACE"]
    tokenize_args = True
    arg_type = int
    arg_req = ArgReqType.ALLOWED

    def verify_arg(self, i: int) -> str | None:
        if not (i > -1 or i < 100):
            return "Whitespace count must be 0 or above, or below 100"

    # def run_compile(
    #     self, commandName: PreLine, arg: int | None
    # ) -> str | list[str] | CompiledReturn | None:
    def run_compile(self, commandName: PreLine, arg: Line | None) -> str | list[str] | CompiledReturn | None:
        if arg is None:
            return ""

        return ["" for _ in range(arg.content)]
