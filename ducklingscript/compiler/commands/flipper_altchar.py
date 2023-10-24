from typing import Any
from ..pre_line import PreLine
from .bases import SimpleCommand


class FlipperAltChar(SimpleCommand):
    names = ["ALTCHAR"]
    flipper_only = True
    arg_type = str

    def verify_arg(self, i: str) -> str | None:
        return (
            None
            if i.strip().isdigit() and len(i.strip()) <= 4
            else "Argument must be a number, and 4 digits or less."
        )
