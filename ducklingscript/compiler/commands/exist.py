from .bases.doc_command import ArgReqType
from ..errors import GeneralError
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from ducklingscript.compiler.tokenization import token_return_types
from .bases import Line, SimpleCommand


class Exist(SimpleCommand):
    names = ["EXIST"]
    arg_req = ArgReqType.REQUIRED

    def run_compile(
        self, commandName: PreLine, arg: Line
    ) -> str | list[str] | CompiledReturn | None:
        if arg.content in self.env.all_vars:
            return

        raise GeneralError(self.stack, f"'{arg}' does not exist.")
