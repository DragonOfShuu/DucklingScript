from .bases import ArgLine, SimpleCommand

desc = """
As if the user was to press the Linux Magic SYSRQ key.
"""


class FlipperSysrq(SimpleCommand):
    names = ["SYSRQ"]
    flipper_only = True
    description = desc

    def verify_arg(self, arg: ArgLine) -> str | None:
        return None if len(arg) == 1 else "This command is one char only"
