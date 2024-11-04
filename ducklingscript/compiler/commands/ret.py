from ducklingscript.compiler.pre_line import PreLine
from .bases import Arguments, ArgLine, SimpleCommand
from ..stack_return import CompiledReturn, StackReturnType
from ..errors import InvalidArgumentsError

desc = """
Exit a function, or your script early.
"""


class Return(SimpleCommand):
    names = ["RETURN", "RET"]
    tokenize_args = True
    description = desc

    def verify_args(self, args: Arguments) -> str | None:
        if len(args) > 1:
            raise InvalidArgumentsError(
                self.stack, "Return statement cannot include more than one argument."
            )

    def run_compile(
        self, command_name: PreLine, arg: ArgLine | None
    ) -> str | list[str] | CompiledReturn | None:
        return_data = None if arg is None else arg.content
        return CompiledReturn(
            return_type=StackReturnType.RETURN, return_data=return_data
        )
