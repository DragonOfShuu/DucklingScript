from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.compiled_ducky import StackReturnType, CompiledDucky
from .bases import BlockCommand, Example
from ..tokenization import Tokenizer
from ..errors import ExceededLimitError

desc = """
Loop a block of code while a condition is true. Optionally 
add a variable to store the amount of previous iterations.
"""

example_list = [
    Example.from_dict(
        {
            "duckling": """
VAR a 10
WHILE a!=15
    VAR a a+1
    $STRING a
""",
            "compiled": """
STRING 11
STRING 12
STRING 13
STRING 14
STRING 15
""",
        }
    ),
    Example.from_dict(
        {
            "duckling": """
VAR a ""
WHILE count,a!="eee"
    VAR a a+"e"
    $STRING a + " [iteration: "+count+"]" 
""",
            "compiled": """
STRING e [iteration: 0]
STRING ee [iteration: 1]
STRING eee [iteration: 2]
""",
        }
    ),
]


class While(BlockCommand):
    names = ["WHILE"]
    description = desc
    examples = example_list
    arg_type = "<condition> or <variable name>,<condition>"

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

    def should_break(self, x: CompiledDucky):
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
        command_name: PreLine,
        argument: str,
        code_block: list[PreLine | list],
    ) -> CompiledDucky | None:
        arg_parts = self.parse_argument(argument)

        var_name: str | None = None
        if isinstance(arg_parts, list):
            var_name, argument = arg_parts

        new_code = CompiledDucky()
        # The actual amount of times
        # the while loop has repeated
        real_count = 0
        # The amount of times the
        # while loop has repeated, +
        # any adjustments the user
        # has made to the env var.
        environment_count = 0
        while True:
            if real_count > 20_000:
                raise ExceededLimitError(
                    self.stack,
                    "Limit was exceeded on while loop. Limit is 20,000 iterations.",
                )

            with self.stack.add_stack_above(code_block) as new_stack:
                if var_name is not None:
                    new_stack.env.var.new_var(var_name, environment_count)

                if not Tokenizer.tokenize(argument, new_stack, new_stack.env):
                    break

                compiled = new_stack.run()

                new_code.append(compiled)

                if self.should_break(new_code):
                    break

            environment_count = (
                new_stack.env.var.all_vars.get(var_name, environment_count) + 1
            )
            real_count += 1
        return new_code
