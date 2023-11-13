from ..errors import GeneralError
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand


class Exist(SimpleCommand):
    names = ["EXIST"]

    def run_compile(
        self, commandName: PreLine, all_args: list[token_return_types]
    ) -> list[str] | CompiledReturn | None:
        for i in all_args:
            if i not in self.env.all_vars:
                # raise CompilationError()
                raise GeneralError(self.stack, f"'{i}' does not exist.")
