from __future__ import annotations
from dataclasses import dataclass

from .pre_line import PreLine
from .errors import StackOverflowError
import ducklingscript.cli.compiler.commands as ScriptCommands


def firstOfList(the_list: list|PreLine) -> PreLine|bool:
    if not isinstance(the_list, list): return the_list
    if len(the_list) == 0: return False

    return firstOfList(the_list[0])

@dataclass
class StackOptions:
    stack_limit: int = 20

class Stack:
    def __init__(self, commands: list[PreLine|list], stack_pile: list[Stack] | None = None, stack_options: StackOptions = StackOptions()):
        # variables: dict[str, str] = {}
        self.commands = commands
        # self.variables = variables

        self.stack_options = stack_options
        self.stack_pile: list[Stack]
        self.current_line: PreLine|None = None
        if stack_pile:
            if len(stack_pile) == self.stack_options.stack_limit: raise StackOverflowError(f"Max amount of stacks reached on {stack_pile[-1].current_line}")

            self.stack_pile = stack_pile
            self.stack_pile.append(self)
        else:
            self.stack_pile = [self]
        
    def start(self):
        returnable: list[str] = []
        can_have_indent: bool = False
        for count,command in enumerate(self.commands):
            if isinstance(command, list):
                if can_have_indent: return
                else: raise IndentationError(f"Unexpected indentation on line {self.current_line if self.current_line!=None else 1}")
            self.current_line = command
            line_num = command.number
            newCommand = command.content.split(maxsplit=1)

            if len(newCommand) > 1:
                pass
                # returnable.append(__BaseCommand(PreLine(newCommand[0], line_num), newCommand[1], ))