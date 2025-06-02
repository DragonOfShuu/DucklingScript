from quackinter.stack import Stack
from pyautogui import hotkey, typewrite, sleep

from ..main import plugin
from quackinter import Command


@plugin.interpretation()
class PowershellInterpretation(Command):
    """
    An example interpretation for the DucklingScript CLI.
    This interpretation does nothing but serves as a template for creating new interpretations.
    """

    @classmethod
    def is_this_command(cls, name: str, data: str) -> bool:
        """
        Check if the command matches this interpretation.
        """
        return name.upper() == "POWERSHELL" and data.strip() == ""

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        hotkey("win", "r")  # Open Run dialog
        sleep(1)
        typewrite("powershell")
        typewrite(["enter"])
        sleep(1)
