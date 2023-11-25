from .bases import Line, SimpleCommand

desc = "As if the user was to press the shift key."

class Shift(SimpleCommand):
    names = ["SHIFT"]
    parameters: list[str] = [
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
    description = desc

    def verify_arg(self, arg: Line) -> str | None:
        if arg.content.upper() not in self.parameters:
            return (
                f"Improper argument. Allowed options are: {', '.join(self.parameters)}"
            )
