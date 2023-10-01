from .pre_line import PreLine

class Command:
    def __init__(self, command: PreLine, argument: str, code_block: list[PreLine]) -> None:
        self.command = command
        self.argument = argument

    def start(self):
        pass