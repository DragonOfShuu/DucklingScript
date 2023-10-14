from typing import Any
from ..pre_line import PreLine
from .base_command import BaseCommand
from ducklingscript.compiler.errors import InvalidArguments


class Delay(BaseCommand):
    names = ["DELAY"]

    @staticmethod
    def verify_arg(i: str) -> str | None:
        return None if i.isdigit() else "A numerical value is required."
