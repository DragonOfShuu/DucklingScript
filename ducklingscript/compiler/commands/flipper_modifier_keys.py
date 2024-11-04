from .bases import ArgLine, SimpleCommand

desc = """
As if the user was to press any of the given combinations. 
Accepts a single character as an argument.
"""


class FlipperModifierKeys(SimpleCommand):
    names = ["CTRL-ALT", "CTRL-SHIFT", "ALT-SHIFT", "ALT-GUI", "GUI-SHIFT"]
    flipper_only = True
    description = desc

    def verify_arg(self, arg: ArgLine) -> str | None:
        return (
            None
            if len(arg.content) == 1
            else "This command only allows 1 character. No more no less."
        )
