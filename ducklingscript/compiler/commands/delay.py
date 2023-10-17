from typing import Any
from ..pre_line import PreLine
from .base_command import BaseCommand
from ducklingscript.compiler.errors import InvalidArguments
from ..tokenization import Tokenizer


class Delay(BaseCommand):
    names = ["DELAY"]

    def verify_arg(self, i: str) -> str | None:
        tokenized = Tokenizer.tokenize(i, self.stack, self.env)
        return None if isinstance(tokenized, int) else "An integer value is required"

    def format_arg(self, arg: str) -> str:
        return str(Tokenizer.tokenize(arg, self.stack, self.env))
