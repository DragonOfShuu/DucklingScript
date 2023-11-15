from ducklingscript.compiler.stack_return import CompiledReturn
from .bases import SimpleCommand


class Rem(SimpleCommand):
    names = ["REM"]

    def multi_comp(self, commandName, all_args) -> list[str] | CompiledReturn | None:
        if self.stack.compile_options.include_comments:
            return super().multi_comp(commandName, all_args)
