
from typing import Any
from ducklingscript.compiler.pre_line import PreLine
from .bases.simple_command import SimpleCommand


class QuackinterGeneralKey(SimpleCommand):
    @classmethod
    def is_this_command(cls, command_name: PreLine, argument: str | None, code_block: list[PreLine] | None, stack: Any | None = None) -> bool:
        try:
            from quackinter import GeneralKeyCommand
        except ImportError:
            return False
        
        return GeneralKeyCommand.is_this_command(command_name.content, '')
