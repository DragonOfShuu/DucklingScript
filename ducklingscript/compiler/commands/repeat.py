from typing import Any

# from ducklingscript.compiler.environment import Environment
from ..environment import Environment
from ..pre_line import PreLine
from .base_command import BaseCommand
from ..errors import InvalidArguments
from ..tokenization import Tokenizer


class Repeat(BaseCommand):
    names = ["REPEAT", "FOR"]
    accept_new_lines = True

    def __init__(self, env: Environment, stack: Any):
        super().__init__(env, stack)
        self.var_name: None | str = None

    def parse_argument(self, argument: str):
        arg = argument.split(",", 1)
        if len(arg) == 1:
            self.sets_variable = False
            return arg[0]

        self.sets_variable = True
        return arg

    def tokenize_count(self, argument):
        tokenized = Tokenizer.tokenize(argument, self.stack, self.env)

        if isinstance(tokenized, float) and tokenized.is_integer():
            tokenized = int(tokenized)

        if not isinstance(tokenized, int):
            raise InvalidArguments(self.stack, "Argument must an integer.")
        if tokenized < 0 or tokenized > 20_000:
            raise InvalidArguments(
                self.stack, "Argument cannot be below 0 or exceed 20,000"
            )
        return tokenized

    def set_count_value(self, count: int):
        if self.var_name is None:
            return

        if self.env.user_vars.get(self.var_name, None) is None:
            # print("Created system var")
            self.env.new_var(self.var_name, count)
            return

        self.env.edit_user_var(self.var_name, count)

    def remove_count_value(self):
        if self.var_name is not None:
            self.env.delete_user_var(self.var_name)
            self.var_name = None

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value
        self.set_count_value(value)
        return self._count

    def run_compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        all_args: list[str],
    ) -> list[str] | None:
        if not argument:
            raise InvalidArguments(self.stack, "An argument is required.")

        arg_parts = self.parse_argument(argument.strip())

        if isinstance(arg_parts, list):
            self.var_name, argument = arg_parts

        if not code_block:
            raise InvalidArguments(
                self.stack, "Tabbed region is required after REPEAT."
            )

        new_code: list[str] = []
        self.count = 0
        while self.count < self.tokenize_count(argument):
            with self.stack.add_stack_above(code_block) as new_stack:
                new_code.extend(new_stack.run())
            self.count = 1 + self.count
        self.remove_count_value()
        return new_code
