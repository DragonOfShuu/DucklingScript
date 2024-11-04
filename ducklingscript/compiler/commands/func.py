from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from .bases import BlockCommand, Example

desc = """
Create a re-runnable block of code. Give arguments to create the function name,
and new variables that can be adjusted at run time. 
Use the RUN command to run your function code.
"""

example_list = [
    Example.from_dict(
        {
            "duckling": """
FUNC hello
    STRING Hello World!

RUN hello
STRING In the middle
RUN hello
""",
            "compiled": """
STRING Hello World!
STRING In the middle
STRING Hello World!
""",
        }
    ),
    Example.from_dict(
        {
            "duckling": """
FUNC hello phrase,number
    $STRING "The number given was: "+number
    $STRING phrase

RUN hello "Foo/Bar",10
""",
            "compiled": """
STRING The number given was: 10
STRING Foo/Bar
""",
        }
    ),
]


class Func(BlockCommand):
    names = ["FUNC", "FUNCTION"]
    description = desc
    arg_type = "<function name>,<variable names...>"

    examples = example_list

    def run_compile(
        self,
        command_name: PreLine,
        argument: str,
        code_block: list[PreLine | list],
    ) -> list[str] | CompiledReturn | None:
        name, var_string = self.break_arg(argument)

        func_vars = self.setup_vars(var_string)

        self.env.var.new_function(name, func_vars, code_block, self.stack.file)

    def setup_vars(self, var_string: str) -> list[str]:
        if not var_string:
            return []

        func_vars = var_string.split(",")
        func_vars = [i.strip() for i in func_vars]
        return func_vars

    def break_arg(self, runnable: str) -> tuple:
        x = runnable.split(" ", maxsplit=1)
        if len(x) == 1:
            return (x[0], None)
        else:
            return x[0], x[1].strip()
