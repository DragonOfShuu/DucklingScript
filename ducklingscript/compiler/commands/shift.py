from ..pre_line import PreLine
from .bases import SimpleCommand


class Shift(SimpleCommand):
    names = ["SHIFT"]
    should_have_args = False
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

    def verify_arg(self, i: str) -> str | None:
        if i.upper() not in self.parameters:
            return (
                f"Improper argument. Allowed options are: {', '.join(self.parameters)}"
            )
