from typing import Any
from ducklingscript.compiler.environment import Environment
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from ...tokenization import Tokenizer, token_return_types
from .base_command import BaseCommand
from abc import abstractmethod


class BlockCommand(BaseCommand):
    accept_new_lines = True
    # tokenize_arg = False

    argument_required = True
    """
    An Argument is required
    for this command (does
    not include the code
    block).
    """
    code_block_required = True
    """
    If the code block after
    this command is a 
    requirement.
    """
    strip_arg = True
    """
    If the argument given
    should be stripped.
    """

    def __init__(self, env: Environment, stack: Any):
        super().__init__(env, stack)
        self.arg: None | str = None

    @property
    def token_arg(self) -> token_return_types:
        if self.arg is None:
            raise TypeError("Argument was tokenized before it was created.")
        return Tokenizer.tokenize(self.arg, self.stack, self.env)

    @classmethod
    def isThisCommand(
        cls,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        stack: Any | None = None,
    ) -> bool:
        if (
            (
                commandName.content.startswith("$")
                and commandName.cont_upper()[1:] in cls.names
            )
            or (cls.argument_required and not argument)
            or (cls.code_block_required and not code_block)
        ):
            return False
        return super().isThisCommand(commandName, argument, code_block)

    def compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine | list] | None,
    ) -> list[str] | CompiledReturn | None:
        super().compile(commandName, argument, code_block)
        if argument and self.strip_arg:
            argument = argument.strip()
        self.arg = argument
        return self.run_compile(commandName, argument, code_block)

    @abstractmethod
    def run_compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine | list] | None,
    ) -> list[str] | CompiledReturn | None:
        pass
