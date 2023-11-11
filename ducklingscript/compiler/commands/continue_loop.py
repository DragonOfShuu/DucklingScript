from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand
from ..stack_return import CompiledReturn, StackReturnType


class ContinueLoop(SimpleCommand):
    names = ["CONTINUE_LOOP","CONTINUELOOP","CONTINUE"]
    can_have_arguments = False

    def run_compile(
        self, commandName: PreLine, all_args: list[token_return_types]
    ) -> list[str] | CompiledReturn | None:
        return CompiledReturn(return_type=StackReturnType.CONTINUE)
