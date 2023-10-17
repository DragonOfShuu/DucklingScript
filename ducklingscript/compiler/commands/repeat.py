from typing import Any
from ..pre_line import PreLine
from .base_command import BaseCommand
from ..errors import InvalidArguments

# from ..environment import Environment
from ..tokenization import Tokenizer


class Repeat(BaseCommand):
    names = ["REPEAT", "FOR"]
    accept_new_lines = True

    def run_compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        all_args: list[str],
    ) -> list[str] | None:
        if not argument:
            raise InvalidArguments(self.stack, "An argument is required.")
        argument = argument.strip()

        def tokenize():
            tokenized = Tokenizer.tokenize(argument, self.stack, self.env)
            if not isinstance(tokenized, int):
                raise InvalidArguments("Argument must an integer.")
            if tokenized < 0 or tokenized > 20_000:
                raise InvalidArguments(
                    self.stack, "Argument cannot be below 0 or exceed 20,000"
                )
            return tokenized

        if not code_block:
            raise InvalidArguments(
                self.stack, "Tabbed region is required after REPEAT."
            )

        new_code: list[str] = []
        count = 0
        while count < tokenize():
            with self.stack.add_stack_above(code_block) as new_stack:
                new_code.extend(new_stack.run())
            count += 1
        return new_code
