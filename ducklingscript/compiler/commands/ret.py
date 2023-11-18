from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.tokenization import token_return_types
from .bases import Arguments, Line, SimpleCommand
from ..stack_return import CompiledReturn, StackReturnType
from ..errors import InvalidArguments


class Return(SimpleCommand):
    names = ["RETURN", "RET"]
    tokenize_args = True

    # def verify(self, commandName, all_args) -> list[str] | CompiledReturn | None:
    # def verify_args(self, args: list[str] | list[token_return_types]) -> str | None:
    def verify_args(self, args: Arguments) -> str | None:
        if len(args) > 1:
            raise InvalidArguments(
                self.stack, "Return statement cannot include more than one argument."
            )

    # def run_compile(
    #     self, commandName: PreLine, arg: token_return_types | None
    # ) -> str | CompiledReturn | None:
    def run_compile(self, commandName: PreLine, arg: Line | None) -> str | list[str] | CompiledReturn | None:
        return_data = None if arg is None else arg.content
        return CompiledReturn(return_type=StackReturnType.RETURN, return_data=return_data)
