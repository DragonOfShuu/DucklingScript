from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand

parameters = ["END", "ESC", "ESCAPE", "SPACE", "TAB"]
parameters.extend([f"F{num}" for num in range(1, 13)])


class Alt(SimpleCommand):
    names = ["ALT"]
    should_have_args = False

    def verify_arg(self, i: str) -> str | None:
        if i.upper() in parameters:
            return None
        elif len(i) == 1:
            return None
        else:
            return f"Legal parameters are either a single character, or one of these: {', '.join(parameters)}"

    def format_arg(self, arg: str) -> str:
        print(f"Arg is: {arg}, parameters are: {parameters}")
        print(arg.upper() in parameters)
        return arg.upper() if arg.upper() in parameters else arg
