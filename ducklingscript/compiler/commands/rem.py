from ducklingscript.compiler.stack_return import CompiledReturn, StackReturnType
from ducklingscript.compiler.tokenization import token_return_types
from ..pre_line import PreLine
from .bases import SimpleCommand


class Rem(SimpleCommand):
    names = ["REM"]

    def run_compile(
        self, commandName: PreLine, all_args: list[token_return_types]
    ) -> list[str] | CompiledReturn | None:
        if self.stack.compile_options.include_comments:
            return super().run_compile(commandName, all_args)
