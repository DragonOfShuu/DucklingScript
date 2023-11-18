from ducklingscript.compiler.tokenization import token_return_types
from .bases import Line, SimpleCommand


class FlipperSysrq(SimpleCommand):
    names = ["SYSRQ"]
    flipper_only = True

    # def verify_arg(self, i: str) -> str | None:
    def verify_arg(self, arg: Line) -> str | None:
        return None if len(arg) == 1 else "This command is one char only"
