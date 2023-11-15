from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand
from ..stack_return import CompiledReturn, StackReturnType
from ..errors import InvalidArguments


class Return(SimpleCommand):
    names = ["RETURN", "RET"]
    tokenize_args = True

    def multi_comp(self, commandName, all_args) -> list[str] | CompiledReturn | None:
        if len(all_args) > 1:
            raise InvalidArguments(
                self.stack, "Return statement cannot include more than one argument."
            )
        return super().multi_comp(commandName, all_args)

    def run_compile(
        self, commandName: PreLine, arg: token_return_types | None
    ) -> str | CompiledReturn | None:
        return CompiledReturn(return_type=StackReturnType.RETURN, return_data=arg)
