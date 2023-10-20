from __future__ import annotations
from pathlib import Path

from .pre_line import PreLine
from .errors import StackOverflowError, WarningsObject
from .commands import command_palette, BaseCommand, ParsedCommand
from .environment import Environment
from .compile_options import CompileOptions
from .stack_return import StackReturn


def firstOfList(the_list: list | PreLine) -> PreLine | bool:
    """
    Recursively finds
    the first item of a
    list of lists.
    """
    if not isinstance(the_list, list):
        return the_list
    if len(the_list) == 0:
        return False

    return firstOfList(the_list[0])


class Stack:
    """
    A class that holds new code
    to run, as well as the current
    environment.
    """

    def __init__(
        self,
        commands: list[PreLine | list],
        file: Path | None = None,
        stack_pile: list[Stack] | None = None,
        owned_by: Stack | None = None,
        compile_options: CompileOptions | None = None,
        warnings: WarningsObject | None = None,
        env: Environment | None = None,
    ):
        self.commands = commands
        self.file = file
        self.warnings = warnings if warnings is not None else WarningsObject()

        self.compile_options = (
            compile_options if compile_options is not None else CompileOptions()
        )
        self.stack_pile: list[Stack]
        self.current_line: PreLine | None = None
        self.next_line: list[PreLine] | PreLine | None = None
        self.owned_stack: Stack | None = None
        self.owned_by: Stack | None = owned_by
        self.env = env if env is not None else Environment(stack=self)
        self.return_type: StackReturn | None = None
        if stack_pile:
            if len(stack_pile) == self.compile_options.stack_limit:
                raise StackOverflowError(
                    self,
                    f"Max amount of stacks reached on {stack_pile[-1].current_line}.\nStack Limit: {self.compile_options.stack_limit}.",
                )

            self.stack_pile = stack_pile
            self.stack_pile.append(self)
        else:
            self.stack_pile = [self]

    def __start(self) -> None:
        """
        Initialize all commands
        in the language through
        the command palette.
        """
        if len(self.stack_pile) != 1:
            return
        for i in command_palette:
            i.initialize(self, self.env)

    def run(self) -> list[str]:
        """
        Beginning the compilation
        process for this stack.
        """
        self.__start()
        returnable: list[str] = []
        leave_stack = False
        for count, command in enumerate(self.commands):
            if leave_stack:
                break
            if isinstance(command, list):
                continue
            self.current_line = command
            self.next_line = (
                None if count + 1 >= len(self.commands) else self.commands[count + 1]
            )
            newCommand = self.__prepare_for_command()

            the_command: BaseCommand | None = None
            for i in command_palette:
                if i.isThisCommand(**newCommand.asdict()):
                    the_command = i(self.env, self)
                    break

            extendable: list[str] | None | StackReturn = None
            if the_command is not None:
                extendable = the_command.compile(**newCommand.asdict())
            else:
                self.warnings.append(
                    f"The command on line {self.current_line.number} may not exist",
                    self.dump_stacktrace(),
                )
                extendable = BaseCommand(self.env, self).compile(**newCommand.asdict())

            if isinstance(extendable, StackReturn):
                self.return_type = extendable
                break

            if extendable:
                returnable.extend(extendable)
        return returnable

    def __prepare_for_command(self) -> ParsedCommand:
        """
        Converts the current line
        of code to a parsed command;
        this will include the command
        name, the argument, and the
        code block after.
        """
        if self.current_line is None:
            raise ValueError(
                "Current line was not initiated. This error should not occur."
            )
        new_command = self.current_line.content.split(maxsplit=1)

        the_command = new_command[0]
        arguments = None if len(new_command) == 1 else new_command[1]
        code_block = None if not isinstance(self.next_line, list) else self.next_line

        return ParsedCommand(
            PreLine(the_command, self.current_line.number), arguments, code_block
        )

    @staticmethod
    def get_stacktrace(stack_pile: list[Stack], limit: int = -1) -> list[str]:
        """
        Gets the stack trace from
        the entire stack pile.
        """
        start_index = (
            0 if limit == -1 or len(stack_pile) <= limit else len(stack_pile) - limit
        )
        stacktrace: list[str] = [
            stack_pile[i].return_stack() for i in range(start_index, len(stack_pile))
        ]
        return stacktrace

    def dump_stacktrace(self, limit: int = -1) -> list[str]:
        """
        Return the stack trace from the
        stack pile according to the limit
        given.
        """
        return self.get_stacktrace(self.stack_pile, limit)

    def return_stack(self):
        """
        Return this stack's traceback
        """
        returnable: list[str] = []
        if not self.current_line:
            return "> Unknown Line"  # Hopefully not possible
        if self.file:
            returnable.append(
                f"In file '{self.file}', on line {self.current_line.number}"
            )
        else:
            returnable.append(f"On line {self.current_line.number}")
        returnable.append(f"> {self.current_line.content}")
        return "\n".join(returnable)

    def add_stack_above(self, commands: list[PreLine | list], file: str | None = None):
        """
        Add a new owned stack
        onto the stack pile.
        """
        self.owned_stack = Stack(
            commands,
            (self.file if not file else Path(file)),
            self.stack_pile,
            self,
            self.compile_options,
            self.warnings,
            self.env.copy(),
        )
        return self.owned_stack

    def remove_stack_above(self):
        """
        Remove the stacks above this
        one. This function should
        only have to destroy one stack
        in total; if it has to destroy
        more, you are doing it wrong.
        """
        if self.owned_stack:
            self.owned_stack.remove_stack_above()
            self.stack_pile.remove(self.owned_stack)
            self.owned_stack = None

    def add_warning(self, warning: str):
        """
        Add a compiler warning
        """
        self.warnings.append(warning, self.dump_stacktrace())

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if self.owned_by and exception_type is None:
            self.owned_by.env.update_from_env(self.env)
            self.owned_by.remove_stack_above()
        return False

    def __iter__(self):
        return self.stack_pile.__iter__()