from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.compiled_ducky import CompiledDucky, StdOutData
from .bases import ArgLine, SimpleCommand

desc = """
Prints out text to the console. Please note that this
does not appear in the compiled file.
"""


class Print(SimpleCommand):
    names = ["PRINT"]
    description = desc

    def run_compile(
        self, command_name: PreLine, arg: ArgLine | None
    ) -> str | list[str] | CompiledDucky | None:
        if arg is None:
            return None

        return CompiledDucky(
            std_out=[
                StdOutData(
                    PreLine(arg.content, arg.line_num, command_name.file_index),
                    self.stack.file,
                )
            ]
        )
