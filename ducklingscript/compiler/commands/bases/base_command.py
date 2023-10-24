# from ducklingscript.cli.compiler.stack import Stack
from ...pre_line import PreLine
from typing import Any
from ducklingscript.compiler.errors import InvalidArguments
from ...environment import Environment
from ...tokenization import Tokenizer
from ...stack_return import StackReturn
from abc import ABC, abstractmethod


class BaseCommand(ABC):
    names: list[str] = []
    """
    Command names to match up with this command.
    
    For example, the rem command would do:
    ```
    names = ["REM"]
    ```
    """
    flipper_only: bool = False
    """
    If this command is only supported for
    the Flipper Zero's version of 
    duckyscript.
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

    @abstractmethod
    def compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine | list] | None,
    ) -> list[str] | None | StackReturn:
        """
        Checks arguments, uses class
        variables to verify arguments,
        and possibly tokenize values.

        DO NOT override this method.
        Instead, change either class
        variables, or override
        `run_compile`.
        """
        pass

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
