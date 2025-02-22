# from ducklingscript.cli.compiler.stack import Stack

from ducklingscript.compiler.commands.bases.doc_command import ComDoc

from ...pre_line import PreLine
from typing import Any
from ducklingscript.compiler.errors import InvalidCommandError
from ...environments.environment import Environment
from ...compiled_ducky import CompiledDucky
from abc import abstractmethod
from .doc_command import DocCommand


class BaseCommand(DocCommand):
    """
    The base for all command types
    in DucklingScript.
    """
    names: list[str] = []
    """
    Command names to match up with this command.
    
    For example, the rem command would do:
    ```
    names = ["REM"]
    ```
    """

    def __init__(self, env: Environment, stack: Any):
        from ...stack import Stack

        self.env = env
        self.stack: Stack = stack

    def is_this_command(
        self,
        command_name: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        stack: Any | None = None,
    ) -> bool: 
        try:
            self.check_validity()
        except InvalidCommandError:
            return False
        
        return self.run_is_this_command(command_name, argument, code_block, stack)

    def run_is_this_command(
        self,
        command_name: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        stack: Any | None = None,
    ) -> bool:
        """
        Check if the command used by the user is
        this command. You most likely don't need
        to override this command; instead, set
        the `names` variable for this class.
        """
        return False if not self.names else (command_name.content_as_upper() in self.names)

    def compile(
        self,
        command_name: PreLine,
        argument: str | None,
        code_block: list[PreLine | list] | None,
    ) -> CompiledDucky | None:
        """
        Checks arguments, uses class
        variables to verify arguments,
        and possibly tokenize values.

        DO NOT override this method when creating commands.
        Instead, change either class
        variables, or override
        `run_compile`.
        """
        self.check_validity()

    @classmethod
    def initialize(cls, stack: Any, env: Environment):
        """
        Register this command's necessary
        attributes.
        """
        cls.init_env(env)

    @classmethod
    def init_env(cls, env: Environment) -> None:
        """
        Used to initialize system_vars
        associated with this command
        """
        return

    def check_validity(self):
        if self.flipper_only and not self.stack.compile_options.flipper_commands:
            raise InvalidCommandError(
                self.stack,
                "Compile mode is set to not allow flipper commands. This command has been marked as flipper only.",
            )
        if self.quackinter_only and not self.stack.compile_options.quackinter_commands:
            raise InvalidCommandError(
                self.stack,
                "Compile mode is set to not allow quackinter commands. This command has been marked as quackinter only.",
            )

    @classmethod
    @abstractmethod
    def get_doc(cls) -> ComDoc:
        pass
