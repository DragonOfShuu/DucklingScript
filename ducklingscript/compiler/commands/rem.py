from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from ducklingscript.compiler.tokenization import token_return_types
from .bases import Line, SimpleCommand


class Rem(SimpleCommand):
    names = ["REM"]

    def run_compile(
        self, commandName: PreLine, arg: Line | None
    ) -> str | list[str] | CompiledReturn | None:
        if self.stack.compile_options.include_comments:
            return super().run_compile(commandName, arg)
