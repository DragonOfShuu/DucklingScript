from .flipper_special_keys import FlipperSpecialKeys
from .bases import ArgLine, SimpleCommand

from .gui import Gui
from .alt import Alt
from .shift import Shift
from .ctrl import Ctrl

desc = """
As if the user was to press any of the given combinations. 
Accepts a single character as an argument.
"""


class FlipperModifierKeys(SimpleCommand):
    names = (
        ["CTRL-ALT", "CTRL-SHIFT", "ALT-SHIFT", "ALT-GUI", "GUI-SHIFT", "GLOBE"]
        + Ctrl.names
        + Shift.names
        + Alt.names
        + Gui.names
    )
    parameters = FlipperSpecialKeys.names
    flipper_only = True
    description = desc

    def format_arg(self, arg: ArgLine) -> ArgLine:
        arg.update(
            arg.content.upper()
            if arg.content.upper() in self.parameters
            else arg.content
        )
        return arg

    def verify_arg(self, arg: ArgLine) -> str | None:
        if arg.content.upper() in self.parameters:
            return None

        return (
            None
            if len(arg.content) == 1
            else "This command only allows 1 character or special keys."
        )
