from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from .bases.doc_command import ArgReqType
from .bases import Line, SimpleCommand

desc = """
As if the user was to press the enter key.
"""


class Enter(SimpleCommand):
    names = ["ENTER"]
    arg_req = ArgReqType.ALLOWED
    description = desc

    arg_type = int

    def run_compile(
        self, command_name: PreLine, arg: Line | None
    ) -> str | list[str] | CompiledReturn | None:
        if arg is None:
            return super().run_compile(command_name, arg)

        return ["ENTER" for i in range(arg.content)]
