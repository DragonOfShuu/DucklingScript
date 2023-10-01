from enum import Enum
from .pre_line import PreLine

class Stack:
    def __init__(self, commands: list[PreLine], variables: dict[str, str]):
        self.commands = commands
        self.variables = variables

    def start(self):
        returnable: list[str] = []
        for command in self.commands:
            pass