from ducklingscript.compiler.pre_line import PreLine
from .base_command import BaseCommand
from ..tokenization import Tokenizer


class Var(BaseCommand):
    names = ["VAR"]

    @staticmethod
    def verify_arg(i: str) -> str | None:
        arg = i.strip().split(maxsplit=1)
        if len(arg) != 2:
            return "The syntax for creating a var goes as follows: VAR <name> <value>"

    def run_compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        all_args: list[str],
    ) -> list[str] | None:
        for i in all_args:
            arg = i.strip().split(maxsplit=1)
            self.env.new_var(arg[0], Tokenizer.tokenize(arg[1], self.stack, self.env))
