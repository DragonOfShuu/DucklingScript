from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand
from ..stack_return import StackReturn


class Break(SimpleCommand):
    names = ["BREAK"]
    can_have_arguments = False

    def run_compile(
        self, commandName: PreLine, all_args: list[token_return_types]
    ) -> list[str] | StackReturn | None:
        return StackReturn.BREAK
