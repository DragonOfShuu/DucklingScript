from typing import Any
from ducklingscript.compiler.pre_line import PreLine
from .base_command import BaseCommand
from ..environment import Environment
from ..tokenization import ExprTokenizer


class Var(BaseCommand):
    names = ["VAR"]

    # @classmethod
    # def verify_args(cls, args: list[str]) -> str | None:
    #     return super().verify_args(args)
    @staticmethod
    def verify_arg(i: str) -> str | None:
        arg = i.strip().split()
        if len(arg) != 2:
            return "The syntax for creating a var goes as follows: VAR <name> <value>"
        # if not Environment.is_var(arg[0]):
        #     return "Not an acceptable variable name. Variables must have only letters, underscores, or numbers (no numbers at the start of the variable name)"

        # return super().verify_arg(i)

    def run_compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        all_args: list[str],
    ) -> list[str] | None:
        for i in all_args:
            arg = i.strip().split()
            self.env.new_var(
                arg[0], ExprTokenizer.tokenize(arg[1], self.stack, self.env)
            )
