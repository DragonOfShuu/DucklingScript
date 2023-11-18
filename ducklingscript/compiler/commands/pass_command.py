from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from ducklingscript.compiler.tokenization import token_return_types
from .bases import Line, SimpleCommand, ArgReqType


class Pass(SimpleCommand):
    names = ["PASS"]
    arg_req = ArgReqType.NOTALLOWED

    def run_compile(self, commandName: PreLine, arg: Line | None) -> str | list[str] | CompiledReturn | None:
        return
