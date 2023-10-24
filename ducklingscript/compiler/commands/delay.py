from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand
from ..tokenization import Tokenizer


class Delay(SimpleCommand):
    names = ["DELAY"]
    tokenize_args = True
    arg_type = int

    def verify_arg(self, i: int) -> str | None:
        # return super().verify_arg(i)
        if i < 0:
            return "Delay value cannot be below 0."

    # def verify_arg(self, i: str) -> str | None:
    #     if not i.isdigit():
    #         return "Argument must be of type integer"

    # def format_arg(self, arg: str) -> str:
    #     return str(Tokenizer.tokenize(arg, self.stack, self.env))
