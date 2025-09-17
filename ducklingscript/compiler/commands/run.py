from ..environments.value_types.wrapped_function import WrappedFunction
from ..environments.env_extend_type import EnvExtendType
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.compiled_ducky import CompiledDucky
from .bases import ArgLine, SimpleCommand, ArgReqType, Example
from ..errors import StackReturnTypeError, InvalidArgumentsError
from ..tokenization import Tokenizer
from ..compiled_ducky import StackReturnType

desc = """
Allows you to run a function. Give the function name, followed
by any arguments the function needs (arguments are separated
by commas).
"""

duckling_ex = [
    """
FUNC hello
    STRING Hello World!

RUN hello
STRING In the middle
RUN hello
""",
    """
FUNC hello phrase,number
    $STRING "The number given was: "+number
    $STRING phrase

RUN hello "Foo/Bar",10
""",
]

compiled_ex = [
    """
STRING Hello World!
STRING In the middle
STRING Hello World!
""",
    """
STRING The number given was: 10
STRING Foo/Bar
""",
]

example_list = [
    Example(duckling=duckling_ex[0], compiled=compiled_ex[0]),
    Example(duckling=duckling_ex[1], compiled=compiled_ex[1]),
]


class Run(SimpleCommand):
    names = ["RUN"]
    arg_req = ArgReqType.REQUIRED
    arg_type = "<function name> or <function name> <arguments...>"
    descriptiono = desc

    examples = example_list

    def run_compile(
        self, command_name: PreLine, arg: ArgLine
    ) -> str | list[str] | CompiledDucky | None:
        name, var_string = self.break_arg(arg.content)
        var_string: str | None

        if var_string is None or not var_string.strip():
            func_vars = []
        else:
            func_vars = Tokenizer.tokenize(var_string, self.stack, self.env)

        if not isinstance(func_vars, list):
            func_vars = [func_vars]

        # new_func = self.env.var.get_var(name)
        new_func = Tokenizer.tokenize(name, self.stack, self.env)
        if not isinstance(new_func, WrappedFunction):
            raise InvalidArgumentsError(self.stack, f"'{name}' is not a function.")

        func = new_func.value
        injectable_environment = new_func.environment

        if len(func.arguments) != len(func_vars):
            raise InvalidArgumentsError(
                self.stack,
                f"{len(func_vars)} arguments were given when {len(func.arguments)} was expected.",
            )

        with self.stack_pile.add_stack_above(
            # Assuming it's a wrapped function...
            # Since we are just breaking off from the original environment from the import,
            # we can just do a normal extend. The "EnvExtendType.HARD" is not needed here, and
            # is instead used in the IMPORT command.
            func.code,
            func.file,
            EnvExtendType.NORMAL,
            injectable_environment,
        ) as st:
            for count, name in enumerate(func.arguments):
                st.env.var.new_user_var(name, func_vars[count])
            compiled = st.run()

        if compiled.return_type in [
            StackReturnType.BREAK,
            StackReturnType.CONTINUE,
        ]:
            raise StackReturnTypeError(
                self.stack,
                "Return type in function cannot be BREAK or CONTINUE",
            )

        compiled.normalize()
        return compiled

    def break_arg(self, runnable: str) -> tuple:
        x = runnable.split(" ", maxsplit=1)
        if len(x) == 1:
            return (x[0], None)
        else:
            return x[0], x[1].strip()
