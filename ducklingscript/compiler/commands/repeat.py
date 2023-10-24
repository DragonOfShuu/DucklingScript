from typing import Any

from ducklingscript.compiler.stack_return import StackReturn

from ..pre_line import PreLine
from .bases import BlockCommand
from ..errors import InvalidArguments
from ..tokenization import Tokenizer


class Repeat(BlockCommand):
    names = ["REPEAT", "FOR"]
    code_block_required = False

    def parse_argument(self, argument: str):
        """
        Convert the argument
        into either:

        A. Simply the Max Count.
        Done by:
        ```
        REPEAT 10
        ```

        B. A variable and a
        max count. Done by:
        ```
        REPEAT i,10
        ```
        """
        arg = argument.split(",", 1)
        if len(arg) == 1:
            return arg[0]

        return arg

    def tokenize_count(self, argument):
        """
        Tokenize the count
        amount given
        """
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

    def run_compile(
        self,
        commandName: PreLine,
        argument: str,
        code_block: list[PreLine | list] | None,
    ) -> list[str] | StackReturn | None:
        arg_parts = self.parse_argument(argument)
        if not code_block:
            if isinstance(arg_parts, list):
                raise InvalidArguments(
                    self.stack,
                    "A variable cannot be given to REPEAT from ducklingscript 1.0. Please include a code block after.",
                )
            return [f"REPEAT {arg_parts}"]

        var_name: str | None = None
        if isinstance(arg_parts, list):
            var_name, argument = arg_parts

        new_code: list[str] = []
        count = 0
        while count < self.tokenize_count(argument):
            with self.stack.add_stack_above(code_block) as new_stack:
                if var_name is not None:
                    new_stack.env.new_var(var_name, count)

                new_code.extend(new_stack.run())
            count = 1 + count
        return new_code
