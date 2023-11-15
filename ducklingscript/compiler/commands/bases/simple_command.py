from enum import Enum
from typing import Any
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn, StackReturnType
from .base_command import BaseCommand
from ...errors import InvalidArguments
from ...tokenization import Tokenizer, token_return_types


class ArgReqType(Enum):
    REQUIRED = 0
    """
    The argument is required
    for the command to run.
    """
    ALLOWED = 1
    """
    The argument is accepted,
    but not necessary.
    """
    NOTALLOWED = 2
    """
    The argument is not 
    acceptable.
    """


class SimpleCommand(BaseCommand):
    # can_have_arguments: bool = True
    # """
    # If this command should have arguments at all

    # If False, then an error will return if args are given
    # """
    # arg_required: bool = True
    # """
    # If the command should have arguments.

    # If False, the command does not need args to show in compiled form.
    # If True, and arguments are not given, the command will not show in
    # the compiled file
    # """
    arg_req: ArgReqType = ArgReqType.ALLOWED
    """
    If the argument should be 
    required, allowed, or 
    not allowed.
    """
    strip_args: bool = True
    """
    Strip all arguments. 
    """
    tokenize_args: bool = False
    """
    If all arguments
    should be tokenized
    """
    arg_type: type[token_return_types] = str

    @classmethod
    def isThisCommand(
        cls,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        stack: Any | None = None,
    ) -> bool:
        command = commandName.cont_upper()
        if command.startswith("$"):
            command = command[1:]
        return super().isThisCommand(
            PreLine(command, commandName.number), argument, code_block, stack
        )

    def compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
    ) -> list[str] | CompiledReturn | None:
        super().compile(commandName, argument, code_block)  # type: ignore
        if commandName.cont_upper().startswith("$"):
            commandName = PreLine(commandName.content[1:], commandName.number)
            self.tokenize_args = True

        all_args = self.listify_args(argument, code_block)
        if self.strip_args:
            all_args = [i.strip() for i in all_args]
        if self.tokenize_args:
            all_args = Tokenizer.tokenize_all(all_args, self.stack, self.env)
            if self.arg_type == str:
                all_args = [str(i) for i in all_args]

        # Check if all_args has anything, but shouldn't
        if all_args and self.arg_req == ArgReqType.NOTALLOWED:
            raise InvalidArguments(
                self.stack,
                f"{commandName.content.upper()} does not have arguments.",
            )
        elif not all_args and self.arg_req == ArgReqType.REQUIRED:
            raise InvalidArguments(
                self.stack, f"{commandName.cont_upper()} requires an argument."
            )

        # Verify arguments
        if message := self.verify_args(all_args):
            raise InvalidArguments(self.stack, message)

        # Run compile on new terms
        return self.multi_comp(commandName, all_args)

    def multi_comp(self, commandName, all_args) -> list[str] | None | CompiledReturn:
        args = [self.format_arg(i) for i in all_args]
        returnable = CompiledReturn()
        if not args:
            args = [None]  # if args is empty, then it is clearly allowed at this point

        for i in args:
            comp = self.run_compile(
                commandName,
                i,
            )
            if comp is None:
                continue

            if isinstance(comp, str):
                returnable.append(CompiledReturn(data=[comp]))
                continue

            if isinstance(comp, list):
                returnable.data.extend(comp)
                continue

            returnable.append(comp)
        return returnable

    def run_compile(
        self,
        commandName: PreLine,
        arg: token_return_types | None,
    ) -> str | list[str] | None | CompiledReturn:
        """
        Returns a list of strings
        for what the compiled
        output should look like.
        """
        if arg is None:
            return f"{commandName.cont_upper()}"
        return f"{commandName.content.upper()} {arg}"

    @staticmethod
    def listify_args(
        argument: str | None, code_block: list[PreLine] | None
    ) -> list[str]:
        """
        Make all arguments into one
        list (this includes the first
        argument).
        """
        new_code_block: list[str] = []
        if argument:
            new_code_block.append(argument)
        if code_block:
            new_code_block.extend(PreLine.convert_from(code_block))
        return new_code_block

    def verify_arg(self, i: token_return_types) -> str | None:
        """
        Return None if the arg is acceptable,
        return an error if it is not
        """
        if self.arg_type == None:
            return None

        if not isinstance(i, self.arg_type):
            return f"Arguments must be of type {self.arg_type}"

    def verify_args(self, args: list[str] | list[token_return_types]) -> str | None:
        for i in args:
            if message := self.verify_arg(i):
                return message
            if isinstance(i, list):
                return 'New lines are not accepted for this command. If you need new lines, please use triple ".'
        return None

    def format_arg(self, arg: token_return_types) -> token_return_types:
        """
        Runs after verify_args;
        allows you to adjust the
        argument into the necessary
        output.
        """
        return arg
