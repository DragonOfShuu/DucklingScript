from typing import Any

from ducklingscript.compiler.tokenization import token_return_types
from ..pre_line import PreLine
from .bases import SimpleCommand

parameters = ["BREAK", "PAUSE", "ESCAPE", "ESC"]
parameters.extend([f"F{num}" for num in range(1, 13)])


class Ctrl(SimpleCommand):
    names = ["CTRL", "CONTROL"]
    should_have_args = False

    def verify_arg(self, i: str) -> str | None:
        if i.upper() in parameters:
            return None
        elif len(i) == 1:
            return None
        else:
            return f"'{i}' is not an acceptable arg. Legal parameters are either a single character, or one of these: {', '.join(parameters)}"

    def format_arg(self, arg: str) -> token_return_types:
        return arg if arg not in parameters else arg.upper()
