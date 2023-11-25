from .bases.doc_command import ArgReqType
from ..errors import GeneralError
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from .bases import Line, SimpleCommand

desc = '''
Creates an error if the given variable name DOES NOT exist.
'''

class Exist(SimpleCommand):
    names = ["EXIST"]
    arg_req = ArgReqType.REQUIRED
    description = desc

    def run_compile(
        self, commandName: PreLine, arg: Line
    ) -> str | list[str] | CompiledReturn | None:
        if arg.content in self.env.all_vars:
            return

        raise GeneralError(self.stack, f"'{arg}' does not exist.")
