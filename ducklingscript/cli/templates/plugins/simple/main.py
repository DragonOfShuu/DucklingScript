"""
SIMPLE TEMPLATE PLUGIN

This is a simple plugin template for DucklingScript.

It includes a command to greet the user and an interpretation to open PowerShell.

This plugin serves as a basic example of how to create commands and interpretations in DucklingScript.

DucklingScript is made up of SimpleCommands and BlockCommands, which are used to compile DucklingScript into Modified DuckyScript 1.0.
-> More info on SimpleCommands and BlockCommands can be found here: https://ducklingscript.dragonofshuu.dev/docs/guides/crash-course/command-types

Once compiled, the DuckyScript can be interpreted by the Quackinter to perform actions on the system, which are implemented via interpretations.
"""

from ducklingscript import Plugin, SimpleCommand, ArgLine, CompiledDucky, PreLine
from quackinter import Command as Interpretation
from quackinter.stack import Stack as QuackStack

from pyautogui import hotkey, typewrite, sleep

plugin = Plugin("simple", description="A simple plugin for demonstration purposes.", version="0.1.0")


@plugin.command()
class GreetCommand(SimpleCommand):
    # This is what the command will be called in DucklingScript.
    # It can be called with `GREET` or `HELLO`.
    names = ["GREET", "HELLO"]

    def run_compile(
            self, 
            command_name: PreLine, 
            arg: ArgLine | None
        ) -> str | list[str] | None | CompiledDucky:

        # This is what the DuckyScript will look like
        return f"STRINGLN Hello, {arg.content if arg else 'World'}!" 


@plugin.command()
class PowershellCommand(SimpleCommand):
    names = ["POWERSHELL", "PS"]
    description = "Open PowerShell."

    def run_compile(
            self, 
            command_name: PreLine, 
            arg: ArgLine | None
        ) -> str | list[str] | None | CompiledDucky:
        # This is what the DuckyScript will look like.
        return "POWERSHELL"
        # We just pass POWERSHELL right through, as 
        # this is what the interpretation will handle.


@plugin.interpretation()
class PowershellInterpretation(Interpretation):
    names = ["POWERSHELL", "PS"]

    def execute(self, stack: QuackStack, cmd: str, data: str) -> None:
        hotkey("win", "r")  
        sleep(1)
        typewrite("powershell")
        typewrite(["enter"])
        sleep(1)


def main() -> Plugin:
    return plugin
