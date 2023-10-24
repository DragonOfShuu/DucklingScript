from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand


class Gui(SimpleCommand):
    names = ["GUI", "WINDOWS", "META"]

    def verify_arg(self, i: str) -> str | None:
        return (
            None if len(i) == 1 else "Only one character is required. No more or less."
        )
