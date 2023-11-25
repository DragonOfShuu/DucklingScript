from .bases.doc_command import ArgReqType
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.tokenization import token_return_types
from .bases import Line, SimpleCommand
from ..stack_return import CompiledReturn, StackReturnType

desc = '''
Continues through a loop, such as a WHILE or FOR/REPEAT loop.
This means to skip the remaining code inside the loop for the
current iteration only.
'''

class ContinueLoop(SimpleCommand):
    names = ["CONTINUE_LOOP", "CONTINUELOOP", "CONTINUE"]
    arg_req = ArgReqType.NOTALLOWED

    def run_compile(
        self, commandName: PreLine, arg: Line | None
    ) -> str | list[str] | CompiledReturn | None:
        return CompiledReturn(return_type=StackReturnType.CONTINUE)
