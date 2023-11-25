from ducklingscript.compiler.pre_line import PreLine
from .bases import Arguments, Line, SimpleCommand
from ..stack_return import CompiledReturn, StackReturnType
from ..errors import InvalidArguments

desc = '''
Exit a function, or your script early.
'''

class Return(SimpleCommand):
    names = ["RETURN", "RET"]
    tokenize_args = True
    description = desc

    def verify_args(self, args: Arguments) -> str | None:
        if len(args) > 1:
            raise InvalidArguments(
                self.stack, "Return statement cannot include more than one argument."
            )

    def run_compile(
        self, commandName: PreLine, arg: Line | None
    ) -> str | list[str] | CompiledReturn | None:
        return_data = None if arg is None else arg.content
        return CompiledReturn(
            return_type=StackReturnType.RETURN, return_data=return_data
        )
