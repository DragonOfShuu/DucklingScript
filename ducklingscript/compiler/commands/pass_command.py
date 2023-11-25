from ducklingscript.compiler.stack_return import CompiledReturn
from ducklingscript.compiler.pre_line import PreLine
from .bases import Line, SimpleCommand, ArgReqType

desc = '''
Placeholder for future code; recommend for functions
that you have not written out yet.
'''

class Pass(SimpleCommand):
    names = ["PASS"]
    arg_req = ArgReqType.NOTALLOWED
    description = desc

    def run_compile(
        self, commandName: PreLine, arg: Line | None
    ) -> str | list[str] | CompiledReturn | None:
        return
