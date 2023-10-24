from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import StackReturn
from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand
from ..tokenization import Tokenizer


class Var(SimpleCommand):
    names = ["VAR"]

    @staticmethod
    def verify_arg(i: str) -> str | None:
        arg = i.strip().split(maxsplit=1)
        if len(arg) != 2:
            return "The syntax for creating a var goes as follows: VAR <name> <value>"

    def run_compile(
        self, commandName: PreLine, all_args: list[str]
    ) -> list[str] | StackReturn | None:
        for i in all_args:
            arg = i.split(maxsplit=1)
            self.env.new_var(arg[0], Tokenizer.tokenize(arg[1], self.stack, self.env))
