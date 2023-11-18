from ..pre_line import PreLine
from .bases import Line, SimpleCommand


class Shift(SimpleCommand):
    names = ["SHIFT"]
    parameters = [
        "DELETE",
        "HOME",
        "INSERT",
        "PAGEUP",
        "PAGEDOWN",
        "WINDOWS",
        "GUI",
        "UPARROW",
        "DOWNARROW",
        "LEFTARROW",
        "RIGHTARROW",
        "TAB",
    ]

    # def verify_arg(self, i: str) -> str | None:
    def verify_arg(self, arg: Line) -> str | None:
        if arg.content.upper() not in self.parameters:
            return (
                f"Improper argument. Allowed options are: {', '.join(self.parameters)}"
            )
