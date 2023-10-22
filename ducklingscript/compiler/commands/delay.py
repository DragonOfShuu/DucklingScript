from typing import Any
from ..pre_line import PreLine
from .base_command import BaseCommand
from ducklingscript.compiler.errors import InvalidArguments
from ..tokenization import Tokenizer


class Delay(BaseCommand):
    names = ["DELAY"]
    tokenize_all_args = True

    def verify_arg(self, i: str) -> str | None:
        if not i.isdigit():
            return "Argument must be of type integer"

    def format_arg(self, arg: str) -> str:
        return str(Tokenizer.tokenize(arg, self.stack, self.env))
