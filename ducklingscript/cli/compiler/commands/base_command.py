# from ducklingscript.cli.compiler.stack import Stack
from ..pre_line import PreLine
from typing import Any, Callable
from ducklingscript.cli.compiler.errors import InvalidArguments


class BaseCommand:
    names: list[str] = []
    should_verify_args: bool = True
    can_have_arguments: bool = True # If False, then an error will return if args are given
    should_have_args: bool = True # If False, the command does not need args to show in compiled form

    @classmethod
    def isThisCommand(
        cls,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
    ) -> bool:
        return False if not cls.names else (commandName.content.upper() in cls.names)

    @classmethod
    def compile(
        cls,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        stack: Any,
    ) -> list[str] | None:
        all_args = BaseCommand.listify_args(argument, code_block)

        if all_args and not cls.can_have_arguments:
            raise InvalidArguments(
                stack,
                f"{commandName.content.upper()} does not have arguments.",
            )
        if cls.should_verify_args and (message := cls.verify_args(all_args)):
            raise InvalidArguments(stack, message)
        return cls.run_compile(commandName, argument, code_block, all_args, stack)

    @classmethod
    def run_compile(
        cls,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        all_args: list[str],
        stack: Any,
    ) -> list[str] | None:
        if not cls.can_have_arguments:
            return [commandName.content.upper()]

        return (
            None
            if cls.should_have_args and not all_args
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
        return None

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
