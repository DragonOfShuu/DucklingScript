# from ducklingscript.cli.compiler.stack import Stack
from ..pre_line import PreLine
from typing import Any, Callable
from ducklingscript.compiler.errors import InvalidArguments
from ..environment import Environment
from ..tokenization import Tokenizer


class BaseCommand:
    names: list[str] = []
    """
    Command names to match up with this command.
    
    For example, the rem command would do:
    ```
    names = ["REM"]
    ```
    """
    can_have_arguments: bool = True
    """
    If this command should have arguments at all

    If False, then an error will return if args are given
    """
    should_have_args: bool = True
    """
    If the command should have arguments.

    If False, the command does not need args to show in compiled form.
    If True, and arguments are not given, the command will not show in
    the compiled file
    """
    flipper_only: bool = False
    """
    If this command is only supported for
    the Flipper Zero's version of 
    duckyscript.
    """
    accept_new_lines: bool = False
    """
    If a code block is expected
    directly after this command.

    For example, if you have a command
    that does a for loop:
    ```
    FOR 5
        STRING
            HELLO WORLD
    ```
    You should set this variable to
    true.
    """
    tokenize_all_args = False
    tokenize_first_arg = False

    def __init__(self, env: Environment, stack: Any):
        self.env = env
        self.stack = stack

    @classmethod
    def isThisCommand(
        cls,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
    ) -> bool:
        command = commandName.cont_upper()
        if command.startswith("$"):
            command = command[1:]
        return False if not cls.names else (command in cls.names)

    def compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
    ) -> list[str] | None:
        command = commandName.cont_upper()
        if command.startswith("$"):
            if not self.accept_new_lines:
                raise InvalidArguments(
                    self.stack,
                    "'$' operator not allowed for commands that require new code blocks.",
                )
            command = command[1:]
            self.tokenize_all_args = True

        arg, block = self.tokenize(argument, code_block)

        all_args = BaseCommand.listify_args(arg, block)

        if all_args and not self.can_have_arguments:
            raise InvalidArguments(
                self.stack,
                f"{commandName.content.upper()} does not have arguments.",
            )
        if message := self.verify_args(all_args):
            raise InvalidArguments(self.stack, message)

        return self.run_compile(
            commandName,
            arg,
            block,
            [self.format_arg(i) for i in all_args],
        )

    def run_compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        all_args: list[str],
        # stack: Any,
    ) -> list[str] | None:
        if not self.can_have_arguments:
            return [commandName.content.upper()]

        return (
            None
            if self.should_have_args and not all_args
            else [f"{commandName.content.upper()} {i}" for i in all_args]
        )

    @staticmethod
    def listify_args(
        argument: str | None, code_block: list[PreLine] | None
    ) -> list[str]:
        new_code_block: list[str] = []
        if argument:
            new_code_block.append(argument)
        if code_block:
            new_code_block.extend(PreLine.convert_from(code_block))
        return new_code_block

    def verify_arg(self, i: str) -> str | None:
        """
        Return None if the arg is acceptable,
        return an error if it is not
        """
        return None

    def verify_args(self, args: list[str]) -> str | None:
        for i in args:
            if message := self.verify_arg(i):
                return message
            if isinstance(i, list) and not self.accept_new_lines:
                return 'New lines are not accepted for this command. If you need new lines, please use triple ".'
        return None

    def format_arg(self, arg: str) -> str:
        return arg

    def all_args(
        self,
        args: list[str],
        exception: Callable[[str], bool],
    ) -> bool:
        """
        Returns True if args pass
        the function. If one fails,
        False is returned instead.
        """
        for i in args:
            if exception(i):
                return False
        return True

    def tokenize(
        self, arg: str | None, block: list[PreLine] | None
    ) -> tuple[str | None, list[PreLine] | None]:
        if not self.tokenize_all_args and not self.tokenize_first_arg:
            return arg, block

        new_arg = arg
        new_block = block

        if (self.tokenize_all_args or self.tokenize_first_arg) and arg is not None:
            new_arg = str(Tokenizer.tokenize(arg, self.stack, self.env))

        if self.tokenize_all_args and block is not None:
            new_block = [
                PreLine(
                    str(Tokenizer.tokenize(i.content, self.stack, self.env)), i.number
                )
                for i in block
            ]

        return (new_arg, new_block)

    @classmethod
    def initialize(cls, stack: Any, env: Environment):
        cls.init_env(env)

    @classmethod
    def init_env(cls, env: Environment) -> None:
        """
        Used to initialize system_vars
        associated with this command
        """
        return
