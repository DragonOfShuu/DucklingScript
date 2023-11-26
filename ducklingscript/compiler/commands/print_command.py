from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn, StdOutData
from .bases import Line, SimpleCommand

desc = """
Prints out text to the console. Please note that this
does not appear in the compiled file.
"""


class Print(SimpleCommand):
    names = ["PRINT"]
    description = desc

    def run_compile(
        self, commandName: PreLine, arg: Line | None
    ) -> str | list[str] | CompiledReturn | None:
        if arg is None:
            return None

        return CompiledReturn(
            std_out=[StdOutData(PreLine(arg.content, arg.line_num), self.stack.file)]
        )
