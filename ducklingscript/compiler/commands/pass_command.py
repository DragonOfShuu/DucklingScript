from ducklingscript.compiler.compiled_ducky import CompiledDucky
from ducklingscript.compiler.pre_line import PreLine
from .bases import ArgLine, SimpleCommand, ArgReqType

desc = """
Placeholder for future code; recommend for functions
that you have not written out yet.
"""


class Pass(SimpleCommand):
    names = ["PASS"]
    arg_req = ArgReqType.NOTALLOWED
    description = desc

    def run_compile(
        self, command_name: PreLine, arg: ArgLine | None
    ) -> str | list[str] | CompiledDucky | None:
        return
