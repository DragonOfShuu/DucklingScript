from typing import Any
from ducklingscript.cli.compiler.pre_line import PreLine
from .base_command import BaseCommand
from ducklingscript.cli.compiler.errors import InvalidArguments


class Repeat(BaseCommand):
    names = ["REPEAT"]
    should_verify_args = False

    # @staticmethod
    # def verify_arg(i: str) -> str | None:
    #     return (
    #         None if i.isdigit() else "Value given must be an integer."
    #     )

    @classmethod
    def run_compile(cls, commandName: PreLine, argument: str | None, code_block: list[PreLine] | None, all_args: list[str], stack: Any) -> list[str] | None:
        if not argument: raise InvalidArguments(stack, "An argument of type integer is required.")
        if not argument.isdigit(): raise InvalidArguments(stack, "Argument must be of type integer.")
        if not code_block: raise InvalidArguments("Tabbed region is required after REPEAT.")

        stack.make_new_stack(code_block)