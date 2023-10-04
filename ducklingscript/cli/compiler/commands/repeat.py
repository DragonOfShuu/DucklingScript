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
    def run_compile(
        cls,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        all_args: list[str],
        stack: Any,
    ) -> list[str] | None:
        if not argument:
            raise InvalidArguments(stack, "An argument of type integer is required.")
        if not argument.isdigit():
            raise InvalidArguments(stack, "Argument must be of type integer.")
        if not code_block:
            raise InvalidArguments(stack, "Tabbed region is required after REPEAT.")

        new_code: list[str] = []
        for _ in range(int(argument)):
            new_stack = stack.add_stack_above(code_block)
            new_code.extend(new_stack.start())
            stack.remove_stack_above()
        return new_code
