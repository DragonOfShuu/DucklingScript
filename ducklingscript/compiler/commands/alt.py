from .bases.doc_command import ArgReqType
from .bases import ArgLine, SimpleCommand

desc = """
As if the user was holding the alt key. Accepts a single character as a parameter as well.
"""


class Alt(SimpleCommand):
    names = ["ALT"]
    arg_req = ArgReqType.ALLOWED
    parameters: list[str] = ["END", "ESC", "ESCAPE", "SPACE", "TAB"]
    parameters.extend([f"F{num}" for num in range(1, 13)])
    description = desc

    def verify_arg(self, arg: ArgLine) -> str | None:
        if arg.content.upper() in self.parameters:
            return None
        elif len(arg.content) == 1:
            return None
        else:
            return f"Legal parameters are either a single character, or one of these: {', '.join(self.parameters)}"

    def format_arg(self, arg: ArgLine) -> ArgLine:
        arg.update(
            arg.content.upper()
            if arg.content.upper() in self.parameters
            else arg.content
        )
        return arg
