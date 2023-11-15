from ..errors import CompilationError, GeneralError
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand, ArgReqType


class NotExist(SimpleCommand):
    names = ["NOTEXIST", "NOT_EXIST"]
    tokenize_args = False
    arg_req = ArgReqType.REQUIRED

    def run_compile(
        self, commandName: PreLine, arg: str
    ) -> str | CompiledReturn | None:
        if arg not in self.env.all_vars:
            return

        raise GeneralError(self.stack, f"'{arg}' does exist.")
