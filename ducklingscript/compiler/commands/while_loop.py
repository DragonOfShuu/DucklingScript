from typing import Any

from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import StackReturnType, CompiledReturn
from .bases.block_command import BlockCommand
from ..tokenization import Tokenizer
from ..errors import ExceededLimitError


class While(BlockCommand):
    names = ["WHILE"]

    @classmethod
    def isThisCommand(
        cls,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        stack: Any | None = None,
    ) -> bool:
        return super().isThisCommand(commandName, argument, code_block, stack)

    def parse_argument(self, argument: str):
        """
        Convert the argument
        into either:

        A. Simply the Max Count.
        Done by:
        ```
        WHILE 10
        ```

        B. A variable and a
        max count. Done by:
        ```
        WHILE i,10
        ```
        """
        arg = argument.split(",", 1)
        if len(arg) == 1:
            return arg[0]

        return arg

    def should_break(self, x: CompiledReturn):
        """
        Returns True if loop should
        be broken.

        Please note that Continues
        and breaks are normalized.
        """
        match (x.return_type):
            case (StackReturnType.CONTINUE):
                x.normalize()
                return False
            case (StackReturnType.BREAK):
                x.normalize()
                return True
            case (StackReturnType.NORMAL):
                return False
            case _:
                return True

    def run_compile(
        self,
        commandName: PreLine,
        argument: str,
        code_block: list[PreLine | list],
    ) -> list[str] | CompiledReturn | None:
        arg_parts = self.parse_argument(argument)

        var_name: str | None = None
        if isinstance(arg_parts, list):
            var_name, argument = arg_parts

        new_code = CompiledReturn()
        count = 0
        while True:
            if count > 20_000:
                raise ExceededLimitError(
                    self.stack,
                    "Limit was exceeded on while loop. Limit is 20,000 iterations.",
                )

            with self.stack.add_stack_above(code_block) as new_stack:
                if var_name is not None:
                    new_stack.env.new_var(var_name, count)

                if not Tokenizer.tokenize(argument, new_stack, new_stack.env):
                    break

                compiled = new_stack.run()

                new_code.append(compiled)

                if self.should_break(new_code):
                    break

            count = 1 + count
        return new_code
