from .bases.doc_command import ArgReqType
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.tokenization import token_return_types
from .bases import Line, SimpleCommand
from ..stack_return import CompiledReturn, StackReturnType


class BreakLoop(SimpleCommand):
    names = ["BREAK_LOOP", "BREAKLOOP"]
    arg_req = ArgReqType.NOTALLOWED

    # def run_compile(
    #     self, commandName: PreLine, arg: token_return_types | None
    # ) -> str | list[str] | CompiledReturn | None:
    def run_compile(
        self, commandName: PreLine, arg: Line | None
    ) -> str | list[str] | CompiledReturn | None:
        return CompiledReturn(return_type=StackReturnType.BREAK)
