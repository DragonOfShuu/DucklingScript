from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand
from ..stack_return import CompiledReturn, StackReturnType


class BreakLoop(SimpleCommand):
    names = ["BREAK_LOOP", "BREAKLOOP"]
    can_have_arguments = False

    def run_compile(
        self, commandName: PreLine, all_args: list[token_return_types]
    ) -> list[str] | CompiledReturn | None:
        return CompiledReturn(return_type=StackReturnType.BREAK)
