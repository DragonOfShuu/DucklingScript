# from ducklingscript.cli.compiler.stack import Stack

from ducklingscript.compiler.commands.bases.doc_command import ComDoc

from ...pre_line import PreLine
from typing import Any
from ducklingscript.compiler.errors import InvalidCommand
from ...environment import Environment
from ...stack_return import CompiledReturn
from abc import abstractmethod
from .doc_command import DocCommand


class BaseCommand(DocCommand):
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

    @classmethod
    def isThisCommand(
        cls,
        commandName: PreLine,
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
        return False if not cls.names else (commandName.cont_upper() in cls.names)

    def compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine | list] | None,
    ) -> list[str] | None | CompiledReturn:
        """
        Checks arguments, uses class
        variables to verify arguments,
        and possibly tokenize values.

        DO NOT override this method.
        Instead, change either class
        variables, or override
        `run_compile`.
        """
        self.check_flipper()

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

    def check_flipper(self):
        if self.flipper_only and not self.stack.compile_options.flipper_commands:
            raise InvalidCommand(
                self.stack,
                "Compile mode is set to not allow flipper commands. This command has been marked as flipper only.",
            )

    @classmethod
    @abstractmethod
    def get_doc(cls) -> ComDoc:
        pass
