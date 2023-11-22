from __future__ import annotations
from collections.abc import Iterator

from dataclasses import dataclass
from typing import Any, Callable

from .doc_command import ComDoc
from .doc_command import ArgReqType
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from .base_command import BaseCommand
from ...errors import InvalidArguments
from ...tokenization import Tokenizer, token_return_types


@dataclass
class Line:
    content: Any
    line_num: int
    original: PreLine

    @classmethod
    def from_preline(cls, x: PreLine):
        return Line(x.content, x.number, x)
    
    def to_preline(self) -> PreLine:
        return PreLine(self.content, self.line_num)
    
    def tokenize(self, stack: Any, env: Any) -> Line:
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
    def __init__(self, stack: Any, arguments: list[Line]|None = None):
        if arguments is None:
            arguments = []
        from ...stack import Stack
        self.stack: Stack = stack
        super().__init__(arguments)
    
    def map_args(self, method: Callable[[Any], Any]):
        new_args = Arguments(self.stack)
        for i in self:
            new_args.append(Line(method(i.content), i.line_num, i.original))
        return new_args

    def map_line_args(self, method: Callable[[Line], Line]):
        new_args = Arguments(self.stack)
        for i in self:
            new_args.append(method(i))
        return new_args

    def tokenize_all(self, stack: Any, env: Any):
        for i in self:
            i: Line
            i.tokenize(stack, env)

    def append(self, __object: Any) -> None:
        if not isinstance(__object, Line):
            raise TypeError("The wrong type was appended to the Arguments object. Only Line is allowed.")
        return super().append(__object)

    def for_args(self) -> Iterator[Line]:
        '''
        WARNING: Added side effect of 
        setting the stack's line_2
        '''
        for arg in self:
            self.stack.line_2 = arg.original
            yield arg
        self.stack.line_2 = None
    
    def __iter__(self) -> Iterator[Line]:
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

        all_args = self.listify_args(argument, code_block, commandName.number)
        if self.strip_args:
            all_args = all_args.map_args(lambda x: x.strip())
        if self.tokenize_args:
            all_args = self.evaluate_args(all_args)

        # Check if all_args has anything, but shouldn't
        self.__verify_all_args(commandName, all_args)

        # Run compile on new terms
        return self.__multi_comp(commandName, all_args)

    def __multi_comp(self, commandName: PreLine, all_args: Arguments) -> list[str] | None | CompiledReturn:
        args = self.format_args(all_args)
        args = args.map_line_args(lambda i: self.format_arg(i))
        returnable = CompiledReturn()
        if not args:
            args = [None]  # if args is empty, then it is clearly allowed at this point

        for i in args:
            self.stack.line_2 = self.stack.current_line if i is None else i.original
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
        arg: Line | None
    ) -> str | list[str] | None | CompiledReturn:
        """
        Returns a list of strings
        for what the compiled
        output should look like.
        """
        if arg is None:
            return f"{commandName.cont_upper()}"
        return f"{commandName.content.upper()} {arg.content}"

    def evaluate_args(self, all_args: Arguments):
        # all_args.tokenize_all(self.stack, self.env)
        for arg in all_args.for_args():
            arg.tokenize(self.stack, self.env)

        if self.arg_type == str:
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
            new_code_block.append(Line(argument, comm_line_num, self.stack.current_line)) # type: ignore
        if code_block:
            new_code_block.extend([Line.from_preline(i) for i in code_block])
        return new_code_block

    def __verify_all_args(self, commandName: PreLine, all_args: Arguments):
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
        if message := self.__verify_args(all_args):
            raise InvalidArguments(self.stack, message)

        if message := self.verify_args(all_args):
            raise InvalidArguments(self.stack, message)

        for i in all_args.for_args():
            if message := self.verify_arg(i):
                raise InvalidArguments(self.stack, message)

    def __verify_arg(self, arg: Line) -> str | None:
        """
        Return None if the arg is acceptable,
        return an error if it is not
        """
        if self.arg_type == None:
            return None

        if not isinstance(arg.content, self.arg_type):
            return f"Arguments must be of type {self.arg_type}"

    def __verify_args(self, args: Arguments) -> str | None:
        for i in args.for_args():
            if message := self.__verify_arg(i):
                return message
            if isinstance(i.content, list):
                return 'New lines are not accepted for this command. If you need new lines, please use triple ".'
        return None

    def verify_args(self, args: Arguments) -> str | None:
        return None

    def verify_arg(self, arg: Line) -> str | None:
        return None

    def format_args(self, args: Arguments) -> Arguments:
        """
        Runs after verify_args;
        allows you to adjust the
        argument into the necessary
        output.
        """
        return args

    def format_arg(self, arg: Line) -> Line:
        """
        Runs after verify_args and format_args;
        allows you to adjust the
        argument into the necessary
        output.
        """
        return arg

    @classmethod
    def get_doc(cls) -> ComDoc:
        return ComDoc(cls.names, cls.arg_type, cls.arg_req, cls.parameters, cls.description, cls.example_duckling, cls.example_compiled)