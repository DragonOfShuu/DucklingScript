from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import StackReturn
from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand


class Whitespace(SimpleCommand):
    names = ["WHITESPACE"]
    tokenize_args = True
    arg_type = int

    def verify_arg(self, i: int) -> str | None:
        if not (i > -1 or i < 100):
            return "Whitespace count must be 0 or above, or below 100"

    # def run_compile(
    #     self,
    #     commandName: PreLine,
    #     argument: str | None,
    #     code_block: list[PreLine] | None,
    #     all_args: list[str],
    # ) -> list[str] | StackReturn | None:
    def run_compile(
        self, commandName: PreLine, all_args: list[token_return_types]
    ) -> list[str] | StackReturn | None:
        args = [int(i) for i in all_args]
        if not args:
            return [""]

        returnable = []
        for i in args:
            returnable.extend(["" for _ in range(i)])
        return returnable
