from .bases.doc_command import ArgReqType
from .bases import Line, SimpleCommand

desc = '''
As if the user was to hold control. Accepts a single character as an argument as well.
'''

class Ctrl(SimpleCommand):
    names = ["CTRL", "CONTROL"]
    arg_req = ArgReqType.ALLOWED
    parameters: list[str] = ["BREAK", "PAUSE", "ESCAPE", "ESC"]
    parameters.extend([f"F{num}" for num in range(1, 13)])
    description = desc

    # def verify_arg(self, i: str) -> str | None:
    def verify_arg(self, arg: Line) -> str | None:
        i = arg.content
        if i.upper() in self.parameters:
            return None
        elif len(i) == 1:
            return None
        else:
            return f"'{i}' is not an acceptable arg. Legal parameters are either a single character, or one of these: {', '.join(self.parameters)}"

    # def format_arg(self, arg: str) -> token_return_types:
    def format_arg(self, arg: Line) -> Line:
        return arg.update_func(
            lambda arg: arg if arg not in self.parameters else arg.upper()
        )
