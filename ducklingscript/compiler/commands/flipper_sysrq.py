from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand


class FlipperSysrq(SimpleCommand):
    names = ["SYSRQ"]
    flipper_only = True

    def verify_arg(self, i: str) -> str | None:
        return None if len(i) == 1 else "This command is one char only"
