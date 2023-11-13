from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand
from ..errors import StackReturnTypeError, VarIsNonExistent, InvalidArguments
from ..tokenization import Tokenizer
from ..stack_return import StackReturnType


class Run(SimpleCommand):
    names = ["RUN"]

    def run_compile(
        self, commandName: PreLine, all_args: list[str]
    ) -> list[str] | CompiledReturn | None:
        returnable = CompiledReturn()
        for line_offset, runs in enumerate(all_args):
            name, var_string = self.break_arg(runs)
            var_string: str | None

            if var_string is None or not var_string.strip():
                func_vars = []
            else:
                func_vars = Tokenizer.tokenize(var_string, self.stack, self.env)

            if not isinstance(func_vars, list):
                func_vars = [func_vars]

            func = self.env.functions.get(name, None)

            if func is None:
                raise VarIsNonExistent(
                    self.stack, f"No such function named '{name}'", line_offset
                )
            if len(func.arguments) != len(func_vars):
                raise InvalidArguments(
                    self.stack,
                    f"{len(func_vars)} arguments were given when {len(func.arguments)} was expected.",
                    line_offset,
                )

            with self.stack.add_stack_above(func.code, func.file) as st:
                for count, name in enumerate(func.arguments):
                    st.env.new_var(name, func_vars[count])
                compiled = st.run()

            if compiled.return_type in [
                StackReturnType.BREAK,
                StackReturnType.CONTINUE,
            ]:
                raise StackReturnTypeError(
                    self.stack,
                    "Return type in function cannot be BREAK or CONTINUE",
                    line_offset,
                )

            returnable.append(compiled)
        returnable.normalize()
        return returnable

    def break_arg(self, runnable: str) -> tuple:
        x = runnable.split(" ", maxsplit=1)
        if len(x) == 1:
            return (x[0], None)
        else:
            return x[0], x[1].strip()
