from ..errors import GeneralError
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand, ArgReqType


class Exist(SimpleCommand):
    names = ["EXIST"]
    arg_req = ArgReqType.REQUIRED

    def run_compile(
        self, commandName: PreLine, arg: str
    ) -> str | CompiledReturn | None:
        if arg in self.env.all_vars:
            return

        raise GeneralError(self.stack, f"'{arg}' does not exist.")
