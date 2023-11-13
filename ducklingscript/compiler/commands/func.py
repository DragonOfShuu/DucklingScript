from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from .bases import BlockCommand


class Func(BlockCommand):
    names = ["FUNC", "FUNCTION"]

    def run_compile(
        self,
        commandName: PreLine,
        argument: str,
        code_block: list[PreLine | list],
    ) -> list[str] | CompiledReturn | None:
        name, var_string = self.break_arg(argument)

        func_vars = self.setup_vars(var_string)

        self.env.new_function(name, func_vars, code_block, self.stack.file)

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
