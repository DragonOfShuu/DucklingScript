# from ducklingscript.cli.compiler.stack import Stack
from ..pre_line import PreLine
from typing import Any, Callable
from ducklingscript.compiler.errors import InvalidArguments
from ..environment import Environment


class BaseCommand:
    names: list[str] = []
    should_verify_args: bool = True
    can_have_arguments: bool = (
        True  # If False, then an error will return if args are given
    )
    should_have_args: bool = (
        True  # If False, the command does not need args to show in compiled form
    )
    flipper_only: bool = False
    accept_new_lines: bool = False

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
        return False if not cls.names else (commandName.content.upper() in cls.names)

    def compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
    ) -> list[str] | None:
        all_args = BaseCommand.listify_args(argument, code_block)

        if all_args and not self.can_have_arguments:
            raise InvalidArguments(
                self.stack,
                f"{commandName.content.upper()} does not have arguments.",
            )
        if self.should_verify_args and (message := self.verify_args(all_args)):
            raise InvalidArguments(self.stack, message)

        return self.run_compile(
            commandName,
            argument,
            code_block,
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

    @staticmethod
    def verify_arg(i: str) -> str | None:
        """
        Return None if the arg is acceptable,
        return an error if it is not
        """
        return None

    @classmethod
    def verify_args(cls, args: list[str]) -> str | None:
        for i in args:
            if message := cls.verify_arg(i):
                return message
            if isinstance(i, list) and not cls.accept_new_lines:
                return 'New lines are not accepted for this command. If you need new lines, please use triple ".'
        return None

    @staticmethod
    def format_arg(arg: str) -> str:
        return arg

    @classmethod
    def all_args(
        cls,
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
