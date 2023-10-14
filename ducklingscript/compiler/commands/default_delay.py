from typing import Any
from ..pre_line import PreLine
from .base_command import BaseCommand
from ducklingscript.compiler.errors import InvalidArguments


class DefaultDelay(BaseCommand):
    names = ["DEFAULT_DELAY", "DEFAULTDELAY"]

    @staticmethod
    def verify_arg(i: str) -> str | None:
        return None if i.isdigit() else "Argument must be of type integer"
