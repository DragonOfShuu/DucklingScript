from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand
from ..tokenization import Tokenizer


class Delay(SimpleCommand):
    names = ["DELAY"]
    tokenize_args = True
    arg_type = int

    def verify_arg(self, i: int) -> str | None:
        if i < 0:
            return "Delay value cannot be below 0."
