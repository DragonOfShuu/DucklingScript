from typing import Any
from .doc_command import ArgReqType, ComDoc
from ducklingscript.compiler.environments.environment import Environment
from ...errors import InvalidArgumentsError
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.compiled_ducky import CompiledDucky
from ...tokenization import Tokenizer, token_return_types
from .base_command import BaseCommand
from abc import abstractmethod


class BlockCommand(BaseCommand):
    """
    Block Commands are commands that come
    with a block scope after the command.

    Block command example:
    ```
    REPEAT 5
        STRINGLN hello world
        STRINGLN goodbye world
    ```
    """

    accept_new_lines = True

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
    arg_req: ArgReqType = ArgReqType.REQUIRED
    """
    Argument requirement
    level.
    """
    arg_type: str | type = "[Unknown]"

    def __init__(self, env: Environment, stack: Any):
        super().__init__(env, stack)
        self.arg: None | str = None

    @property
    def token_arg(self) -> token_return_types:
        """
        Give the argument that was
        given to this command
        evaluated.

        If the argument is 2+2,
        this will answer 4.
        """
        if self.arg is None:
            raise TypeError("Argument was tokenized before it was created.")
        return Tokenizer.tokenize(self.arg, self.stack, self.env)

    def run_is_this_command(
        self,
        command_name: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        stack: Any | None = None,
    ) -> bool:
        """
        If this command belongs to the
        code found on this line.

        Returns:
            bool, whether the given data
            means we are truly looking at
            this command.
        """
        if (
            command_name.content.startswith("$")
            and command_name.content_as_upper()[1:] in self.names
        ) or (self.code_block_required and not code_block):
            return False
        return super().run_is_this_command(command_name, argument, code_block)

    def compile(
        self,
        command_name: PreLine,
        argument: str | None,
        code_block: list[PreLine | list] | None,
    ) -> CompiledDucky | None:
        super().compile(command_name, argument, code_block)

        if argument and self.arg_req == ArgReqType.NOTALLOWED:
            raise InvalidArgumentsError(
                self.stack, "Arguments are not allowed for this command"
            )
        elif not argument and self.arg_req == ArgReqType.REQUIRED:
            raise InvalidArgumentsError(
                self.stack, "Arguments are required for this command"
            )

        if argument and self.strip_arg:
            argument = argument.strip()
        self.arg = argument

        return self.run_compile(command_name, argument, code_block)

    @abstractmethod
    def run_compile(
        self,
        command_name: PreLine,
        argument: str | None,
        code_block: list[PreLine | list] | None,
    ) -> CompiledDucky | None:
        pass

    @classmethod
    def get_doc(cls) -> ComDoc:
        return ComDoc(
            cls.names,
            cls.flipper_only,
            cls.quackinter_only,
            cls.arg_type,
            cls.arg_req,
            cls.parameters,
            cls.description or cls.__doc__ or "A block command.",
            cls.examples,
        )
