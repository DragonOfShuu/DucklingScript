from typing import Any
from ..pre_line import PreLine
from .base_command import BaseCommand
from ..errors import InvalidArguments


class Repeat(BaseCommand):
    names = ["REPEAT"]
    should_verify_args = False
    accept_new_lines = True

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
        if not argument.strip().isdigit():
            raise InvalidArguments(stack, "Argument must be of type integer.")
        if int(argument) < 0 or int(argument) > 20_000:
            raise InvalidArguments(stack, "Argument cannot be below 0 or exceed 20,000")
        if not code_block:
            raise InvalidArguments(stack, "Tabbed region is required after REPEAT.")

        new_code: list[str] = []
        for _ in range(int(argument.strip())):
            with stack.add_stack_above(code_block) as new_stack:
                new_code.extend(new_stack.start())
        return new_code
