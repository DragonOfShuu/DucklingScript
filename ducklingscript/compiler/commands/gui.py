from ducklingscript.compiler.tokenization import token_return_types
from .bases import Line, SimpleCommand


class Gui(SimpleCommand):
    names = ["GUI", "WINDOWS", "META"]

    # def verify_arg(self, i: str) -> str | None:
    def verify_arg(self, arg: Line) -> str | None:
        return (
            None if len(arg) == 1 else "Only one character is required. No more or less."
        )
