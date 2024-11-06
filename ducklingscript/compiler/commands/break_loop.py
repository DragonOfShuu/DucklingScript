from .bases.doc_command import ArgReqType
from ducklingscript.compiler.pre_line import PreLine
from .bases import ArgLine, SimpleCommand
from ..stack_return import CompiledDucky, StackReturnType

desc = """
Escape a loop, such as a WHILE or FOR/REPEAT loop.
"""


class BreakLoop(SimpleCommand):
    names = ["BREAK_LOOP", "BREAKLOOP"]
    arg_req = ArgReqType.NOTALLOWED
    description = desc

    def run_compile(
        self, command_name: PreLine, arg: ArgLine | None
    ) -> str | list[str] | CompiledDucky | None:
        return CompiledDucky(return_type=StackReturnType.BREAK)
