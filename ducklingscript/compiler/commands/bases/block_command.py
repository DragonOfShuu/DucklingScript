from typing import Any
from ducklingscript.compiler.pre_line import PreLine
from ...errors import InvalidArguments
from ducklingscript.compiler.stack_return import StackReturn
from .base_command import BaseCommand


class BlockCommand(BaseCommand):
    accept_new_lines = True
    tokenize_arg = True

    @classmethod
    def isThisCommand(
        cls,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        stack: Any | None = None,
    ) -> bool:
        if commandName.content.startswith("$") and commandName.cont_upper()[1:] in cls.names:
            raise InvalidArguments(
                stack,
                "'$' operator not allowed for commands that require new code blocks.",
            )
        return super().isThisCommand(commandName, argument, code_block)

    # def compile(self, commandName: PreLine, argument: str | None, code_block: list[PreLine] | None) -> list[str] | StackReturn | None:
    #     # return super().compile(commandName, argument, code_block)
