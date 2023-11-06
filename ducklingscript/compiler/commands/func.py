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
        name, var_string = argument.split(" ", maxsplit=1)

        func_vars = self.setup_vars(var_string)

        self.env.new_function(name, func_vars, code_block)

    def setup_vars(self, var_string: str) -> list[str]:
        if not var_string:
            return []

        func_vars = var_string.split(",")
        func_vars = [i.strip() for i in func_vars]
        return func_vars
