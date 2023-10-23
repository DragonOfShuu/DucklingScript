from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import StackReturn
from .base_command import BaseCommand
from ..tokenization import Tokenizer


class Whitespace(BaseCommand):
    names = ["WHITESPACE"]
    tokenize_all_args = True

    def verify_arg(self, i: str) -> str | None:
        if not i.isdigit():
            return "Argument is required to be of type integer"
        x = int(i)
        if not (x>-1 or x<100):
            return "Whitespace count must be 0 or above, or below 100"

    def run_compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        all_args: list[str],
    ) -> list[str] | StackReturn | None:
        args = [int(i) for i in all_args]
        if not args:
            return [""]

        returnable = []
        for i in args:
            returnable.extend(["" for j in range(i)])
        return returnable
