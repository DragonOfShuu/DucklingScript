from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from .bases import Line, SimpleCommand

desc = """
Create a comment for your code. You can put anything you like
as an argument, if any.
"""


class Rem(SimpleCommand):
    names = ["REM"]
    description = desc

    def run_compile(
        self, command_name: PreLine, arg: Line | None
    ) -> str | list[str] | CompiledReturn | None:
        if self.stack.compile_options.include_comments:
            return super().run_compile(command_name, arg)
