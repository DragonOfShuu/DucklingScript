from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.compiled_ducky import CompiledDucky
from .bases import ArgLine, SimpleCommand

desc = """
Create a comment for your code. You can put anything you like
as an argument, if any.
"""


class Rem(SimpleCommand):
    names = ["REM"]
    description = desc

    def run_compile(
        self, command_name: PreLine, arg: ArgLine | None
    ) -> str | list[str] | CompiledDucky | None:
        if self.stack.compile_options.include_comments:
            return super().run_compile(command_name, arg)
