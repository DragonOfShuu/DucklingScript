from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand, ArgReqType

parameters = ["BREAK", "PAUSE", "ESCAPE", "ESC"]
parameters.extend([f"F{num}" for num in range(1, 13)])


class Ctrl(SimpleCommand):
    names = ["CTRL", "CONTROL"]
    arg_req = ArgReqType.ALLOWED

    def verify_arg(self, i: str) -> str | None:
        if i.upper() in parameters:
            return None
        elif len(i) == 1:
            return None
        else:
            return f"'{i}' is not an acceptable arg. Legal parameters are either a single character, or one of these: {', '.join(parameters)}"

    def format_arg(self, arg: str) -> token_return_types:
        return arg if arg not in parameters else arg.upper()
