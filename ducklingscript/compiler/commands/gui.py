from .bases import ArgLine, SimpleCommand

desc = """
As if the user was to press the windows/meta key.
"""


class Gui(SimpleCommand):
    names = ["GUI", "WINDOWS", "META"]
    description = desc

    def verify_arg(self, arg: ArgLine) -> str | None:
        return (
            None
            if len(arg) == 1
            else "Only one character is required. No more or less."
        )
