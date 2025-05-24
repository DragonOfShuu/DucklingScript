from typing import Any
from ducklingscript.compiler.pre_line import PreLine
from .bases.simple_command import SimpleCommand

desc = """
Added by Quackinter to add support for more
keys
"""


class QuackinterGeneralKey(SimpleCommand):
    quackinter_only = True
    names = []
    description = desc
    try:
        from quackinter import GeneralKeyCommand

        names = GeneralKeyCommand.names[::-1]
    except ImportError:
        names = []

    @classmethod
    def run_is_this_command(
        cls,
        command_name: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        stack: Any | None = None,
    ) -> bool:
        try:
            from quackinter import GeneralKeyCommand
        except ImportError:
            return False

        return GeneralKeyCommand.is_this_command(command_name.content, argument or "")
