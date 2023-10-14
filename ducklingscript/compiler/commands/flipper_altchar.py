from typing import Any
from ..pre_line import PreLine
from .base_command import BaseCommand


class FlipperAltChar(BaseCommand):
    names = ["ALTCHAR"]
    flipper_only = True

    @staticmethod
    def verify_arg(i: str) -> str | None:
        return (
            None
            if i.strip().isdigit() and len(i.strip()) <= 4
            else "Argument must be a number, and 4 digits or less."
        )

    @staticmethod
    def format_arg(arg: str) -> str:
        return arg.strip()
