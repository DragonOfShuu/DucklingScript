from .bases.doc_command import ArgReqType
from ducklingscript.compiler.pre_line import PreLine
from .bases import ArgLine, SimpleCommand
from ..stack_return import CompiledDucky, StackReturnType

desc = """
Continues through a loop, such as a WHILE or FOR/REPEAT loop.
This means to skip the remaining code inside the loop for the
current iteration only.
"""


class ContinueLoop(SimpleCommand):
    names = ["CONTINUE_LOOP", "CONTINUELOOP", "CONTINUE"]
    arg_req = ArgReqType.NOTALLOWED

    def run_compile(
        self, command_name: PreLine, arg: ArgLine | None
    ) -> str | list[str] | CompiledDucky | None:
        return CompiledDucky(return_type=StackReturnType.CONTINUE)
