from ducklingscript.compiler.stack_return import StackReturnType, CompiledReturn

from ..pre_line import PreLine
from .bases import BlockCommand, Example
from ..errors import InvalidArguments
from ..tokenization import Tokenizer

desc = """
Repeats the block of code (or line above, although that syntax is not recommended) a fixed number of times. Give the amount of
times to run as an argument to repeat.

Moreover, you can count the amount of iterations that repeat has already
completed by giving a variable name, then a iteration count separated by 
a comma.
"""

duckling_ex = [
    """
REPEAT 3
    STRING Not only can I repeat...
    STRING ...but so can I!
""",
    """
REPEAT i,3
    $STRING "this is iteration number "+i+"!" 
""",
]

compiled_ex = [
    """
STRING Not only can I repeat...
STRING ...but so can I!
STRING Not only can I repeat...
STRING ...but so can I!
STRING Not only can I repeat...
STRING ...but so can I!
""",
    """
STRING this is iteration number 0!
STRING this is iteration number 1!
STRING this is iteration number 2!
""",
]

example_list = [
    Example(duckling=duckling_ex[0], compiled=compiled_ex[0]),
    Example(duckling=duckling_ex[1], compiled=compiled_ex[1]),
]


class Repeat(BlockCommand):
    names = ["REPEAT", "FOR"]
    code_block_required = False
    description = desc
    arg_type = "<iteration count> or <variable name>,<iteration count>"
    examples = example_list

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
        code_block: list[PreLine | list] | None,
    ) -> list[str] | CompiledReturn | None:
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

        new_code: CompiledReturn = CompiledReturn()
        count = 0
        while count < self.tokenize_count(argument):
            with self.stack.add_stack_above(code_block) as new_stack:
                if var_name is not None:
                    new_stack.env.new_var(var_name, count)

                new_code.append(new_stack.run())

                if self.should_break(new_code):
                    break

            count += 1

        return new_code
