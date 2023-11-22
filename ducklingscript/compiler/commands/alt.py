from .bases.doc_command import ArgReqType
from ducklingscript.compiler.tokenization import token_return_types
from .bases import Line, SimpleCommand

parameters = ["END", "ESC", "ESCAPE", "SPACE", "TAB"]
parameters.extend([f"F{num}" for num in range(1, 13)])


class Alt(SimpleCommand):
    names = ["ALT"]
    arg_req = ArgReqType.ALLOWED

    def verify_arg(self, arg: Line) -> str | None:
        if arg.content.upper() in parameters:
            return None
        elif len(arg.content) == 1:
            return None
        else:
            return f"Legal parameters are either a single character, or one of these: {', '.join(parameters)}"

    def format_arg(self, arg: Line) -> Line:
        arg.update(
            arg.content.upper() if arg.content.upper() in parameters else arg.content
        )
        return arg
