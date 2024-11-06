from __future__ import annotations
from collections.abc import Iterator

from dataclasses import dataclass
from typing import Any, Callable

from .doc_command import ComDoc
from .doc_command import ArgReqType
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledDucky, CompiledDuckyLine
from .base_command import BaseCommand
from ...errors import InvalidArgumentsError
from ...tokenization import Tokenizer, token_return_types


@dataclass
class ArgLine:
    content: Any
    line_num: int
    original: PreLine

    @classmethod
    def from_preline(cls, x: PreLine):
        return ArgLine(x.content, x.number, x)

    def to_preline(self) -> PreLine:
        return PreLine(self.content, self.line_num, self.original.file_index)

    def tokenize(self, stack: Any, env: Any) -> ArgLine:
        self.content = Tokenizer.tokenize(self.content, stack, env)
        return self

    def update(self, content: Any):
        self.content = content
        return self

    def update_func(self, change: Callable[[Any], Any]):
        self.content = change(self.content)
        return self

    def __repr__(self) -> str:
        return self.content

    def __len__(self):
        if not isinstance(self.content, str):
            raise TypeError("Cannot get the length of a line that is not a string.")
        return self.content.__len__()


class Arguments(list):
    def __init__(self, stack: Any, arguments: list[ArgLine] | None = None):
        if arguments is None:
            arguments = []
        from ...stack import Stack

        self.stack: Stack = stack
        super().__init__(arguments)

    def map_args(self, method: Callable[[Any], Any]):
        new_args = Arguments(self.stack)
        for i in self:
            new_args.append(ArgLine(method(i.content), i.line_num, i.original))
        return new_args

    def map_line_args(self, method: Callable[[ArgLine], ArgLine]):
        new_args = Arguments(self.stack)
        for i in self:
            new_args.append(method(i))
        return new_args

    def tokenize_all(self, stack: Any, env: Any):
        for i in self:
            i: ArgLine
            i.tokenize(stack, env)

    def append(self, __object: Any) -> None:
        if not isinstance(__object, ArgLine):
            raise TypeError(
                "The wrong type was appended to the Arguments object. Only Line is allowed."
            )
        return super().append(__object)

    def for_args(self) -> Iterator[ArgLine]:
        """
        WARNING: Added side effect of
        setting the stack's line_2
        """
        for arg in self:
            self.stack.line_2 = arg.original
            yield arg
        self.stack.line_2 = None

    def __iter__(self) -> Iterator[ArgLine]:
        return super().__iter__()


class SimpleCommand(BaseCommand):
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
    arg_type: type[token_return_types] | str = str

    @classmethod
    def is_this_command(
        cls,
        command_name: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        stack: Any | None = None,
    ) -> bool:
        """
        If this command belongs to the
        code found on this line.

        Returns:
            Boolean
        """
        command = command_name.cont_upper()
        if command.startswith("$"):
            command = command[1:]
        return super().is_this_command(
            PreLine(command, command_name.number, command_name.file_index), argument, code_block, stack
        )

    def compile(
        self,
        command_name: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
    ) -> CompiledDucky | None:
        """
        Convert the given DucklingScript
        into Ducky Script 1.0
        """
        super().compile(command_name, argument, code_block)  # type: ignore
        if command_name.cont_upper().startswith("$"):
            command_name = PreLine(command_name.content[1:], command_name.number, command_name.file_index)
            self.tokenize_args = True

        all_args = self.listify_args(argument, code_block, command_name.number)
        if self.strip_args:
            all_args = all_args.map_args(lambda x: x.strip())
        if self.tokenize_args:
            all_args = self.evaluate_args(all_args)

        # Check if all_args has anything, but shouldn't
        self.__verify_all_args(command_name, all_args)

        # Run compile on new terms
        return self.__multi_comp(command_name, all_args)

    def __multi_comp(
        self, command_name: PreLine, all_args: Arguments
    ) -> None | CompiledDucky:
        """
        Return multiple lines of code
        based on the amount of arguments.

        Example:
        ```
        STRINGLN
            Hello World
            Hello World
        ```
        Compiled:
        ```
        STRINGLN Hello World
        STRINGLN Hello World
        ```

        Hello World x2 are the arguments
        """
        args = self.format_args(all_args)
        args = args.map_line_args(lambda i: self.format_arg(i))
        returnable = CompiledDucky()
        if not args:
            args = [None]  # if args is empty, then it is clearly allowed at this point

        for i in args:
            self.stack.line_2 = self.stack.current_line if i is None else i.original
            comp = self.run_compile(
                command_name,
                i,
            )

            if comp is None:
                continue

            line_2 = i.to_preline() if i is not None else None

            if isinstance(comp, str):
                returnable.append(CompiledDucky(data=[CompiledDuckyLine(command_name, comp, line_2)]))
                continue

            if isinstance(comp, list):
                returnable.data.extend([CompiledDuckyLine(command_name, ducky_line, line_2) for ducky_line in comp])
                continue

            returnable.append(comp)
        return returnable

    def run_compile(
        self, command_name: PreLine, arg: ArgLine | None
    ) -> str | list[str] | None | CompiledDucky:
        """
        Returns a string or list of strings
        for what the compiled output should look like.
        """
        if arg is None:
            return f"{command_name.cont_upper()}"
        return f"{command_name.content.upper()} {arg.content}"

    def evaluate_args(self, all_args: Arguments):
        """
        Tokenizes all of the given arguments.

        WARNING: Sets stacks `line_2` as a
        side effect.
        """
        for arg in all_args.for_args():
            arg.tokenize(self.stack, self.env)

        if self.arg_type is str:
            all_args = all_args.map_args(lambda i: str(i))

        return all_args

    def listify_args(
        self, argument: str | None, code_block: list[PreLine] | None, comm_line_num: int
    ) -> Arguments:
        """
        Make all arguments into one
        list (this includes the first
        argument).
        """
        new_code_block: Arguments = Arguments(self.stack)
        if argument:
            new_code_block.append(ArgLine(argument, comm_line_num, self.stack.current_line))  # type: ignore
        if code_block:
            new_code_block.extend([ArgLine.from_preline(i) for i in code_block])
        return new_code_block

    def __verify_all_args(self, command_name: PreLine, all_args: Arguments):
        """
        Arguments are verified in teh following order:

        1. `self.arg_req`
        2. `self.arg_type`
        3. self.verify_args()
        4. self.verify_arg()
        """
        if all_args and self.arg_req == ArgReqType.NOTALLOWED:
            raise InvalidArgumentsError(
                self.stack,
                f"{command_name.content.upper()} does not have arguments.",
            )
        elif not all_args and self.arg_req == ArgReqType.REQUIRED:
            raise InvalidArgumentsError(
                self.stack, f"{command_name.cont_upper()} requires an argument."
            )

        # Verify arguments
        if message := self.__verify_args(all_args):
            raise InvalidArgumentsError(self.stack, message)

        if message := self.verify_args(all_args):
            raise InvalidArgumentsError(self.stack, message)

        for i in all_args.for_args():
            if message := self.verify_arg(i):
                raise InvalidArgumentsError(self.stack, message)

    def __verify_arg(self, arg: ArgLine) -> str | None:
        """
        Return None if the arg is acceptable,
        return an error if it is not
        """
        if self.arg_type is None:
            return None

        if not (
            isinstance(self.arg_type, str) or isinstance(arg.content, self.arg_type)
        ):
            return f"Arguments must be of type {self.arg_type}"

    def __verify_args(self, args: Arguments) -> str | None:
        for i in args.for_args():
            if message := self.__verify_arg(i):
                return message
            if isinstance(i.content, list):
                return "New lines are not accepted for this command. If you need new lines, please use triple quotations."
        return None

    def verify_args(self, args: Arguments) -> str | None:
        return None

    def verify_arg(self, arg: ArgLine) -> str | None:
        return None

    def format_args(self, args: Arguments) -> Arguments:
        """
        Runs after verify_args;
        allows you to adjust the
        argument into the necessary
        output.
        """
        return args

    def format_arg(self, arg: ArgLine) -> ArgLine:
        """
        Runs after verify_args and format_args;
        allows you to adjust the
        argument into the necessary
        output.
        """
        return arg

    @classmethod
    def get_doc(cls) -> ComDoc:
        return ComDoc(
            cls.names,
            cls.flipper_only,
            cls.arg_type,
            cls.arg_req,
            cls.parameters,
            cls.description,
            cls.examples,
        )
