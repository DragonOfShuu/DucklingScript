from __future__ import annotations
from pathlib import Path
from dataclasses import asdict, dataclass

from .pre_line import PreLine
from .errors import StackOverflowError, StackTraceNode, WarningsObject
from .commands import command_palette, BaseCommand, SimpleCommand
from .environments.environment import Environment
from .compile_options import CompileOptions
from .compiled_ducky import StackReturnType, CompiledDucky, StdOutData


@dataclass
class ParsedCommand:
    command_name: PreLine
    argument: str | None = None
    code_block: list[PreLine] | None = None

    def asdict(self):
        return asdict(self)


def first_of_list(the_list: list | PreLine) -> PreLine | bool:
    """
    Recursively finds
    the first item of a
    list of lists.
    """
    if not isinstance(the_list, list):
        return the_list
    if len(the_list) == 0:
        return False

    return first_of_list(the_list[0])


class Stack:
    """
    A class that compiles code
    within an environment. Creates
    new stacks above this one when
    necessary.

    Args:
        duckling: A list of prelines, or a list of a list of prelines, or a li...
        file: The file that is being ran at
        stack_pile: The stack of stacks
        owned_by: The stack that owns this one.
        compile_options: The compilation parameters provided
        warnings: An object storing all warnings with a stacktrace for the warnings
        env: The environment to run the stack within
        parallel: Whether this stack runs in the same environment as the one below it or not. (functions are not parallel, starting code using STARTENV is (we pull all vars from STARTENV directly into this one))
        std_out: The output to show to the console.
    """

    def __init__(
        self,
        duckling: list[PreLine | list],
        file: Path | None = None,
        stack_pile: list[Stack] | None = None,
        owned_by: Stack | None = None,
        compile_options: CompileOptions | None = None,
        warnings: WarningsObject | None = None,
        env: Environment | None = None,
        parallel: bool = False,
        std_out: list[StdOutData] | None = None,
    ):
        self.duckling = duckling
        self.warnings = warnings if warnings is not None else WarningsObject()

        self.compile_options = (
            compile_options if compile_options is not None else CompileOptions()
        )
        self.stack_pile: list[Stack]
        self.current_line: PreLine | None = None
        self.next_line: list[PreLine] | PreLine | None = None
        self.owned_stack: Stack | None = None
        self.owned_by: Stack | None = owned_by
        if file and not file.is_file():
            raise TypeError("File given to Stack is required to be a file.")
        self.file = file
        self.env = env if env is not None else Environment(stack=self)
        self.parallel = parallel
        self.std_out: list[StdOutData] = [] if std_out is None else std_out
        self.line_2: PreLine | None = None
        """
        The secondary line that
        can be defined by an
        inner command. 

        Mainly used for determining
        the location of an error.
        """

        self.return_type: StackReturnType | None = None
        if stack_pile:
            self.stack_pile = stack_pile
            if len(stack_pile) == self.compile_options.stack_limit:
                raise StackOverflowError(
                    self,
                    f"Max stack count was exceeded. (Stack Limit: {self.compile_options.stack_limit})",
                )
            self.stack_pile.append(self)
        else:
            self.stack_pile = [self]

    def start_base(self, run_init: bool = True) -> CompiledDucky:
        if run_init:
            for i in command_palette:
                i.initialize(self, self.env)

        x = self.run()

        if not (
            x.return_type == StackReturnType.NORMAL
            or x.return_type == StackReturnType.RETURN
        ):
            self.warnings.append(
                f"Program was exited using {x.return_type.name} instead of using RETURN"
            )

        return x

    def run(self) -> CompiledDucky:
        """
        Beginning the compilation
        process for this stack.
        """
        returnable: CompiledDucky = CompiledDucky()
        leave_stack = False
        for count, command in enumerate(self.duckling):
            self.line_2: PreLine | None = None

            if leave_stack:
                break
            if isinstance(command, list):
                continue
            self.current_line = command
            self.next_line = (
                None if count + 1 >= len(self.duckling) else self.duckling[count + 1]
            )
            new_command = self.__prepare_for_command()

            the_command: BaseCommand | None = None
            for i in command_palette:
                initted_command = i(self.env, self)
                if initted_command.is_this_command(**new_command.asdict()):
                    the_command = initted_command
                    break

            new_compiled: None | CompiledDucky = None
            if the_command is not None:
                new_compiled = the_command.compile(**new_command.asdict())
            else:
                self.make_not_exist_warn()
                new_compiled = SimpleCommand(self.env, self).compile(
                    **new_command.asdict()
                )

            if new_compiled is None:
                continue

            returnable.append(new_compiled, include_std=False)
            self.std_out.extend(new_compiled.std_out)

            if returnable.return_type == StackReturnType.NORMAL:
                continue
            break

        if (
            self.owned_by
            and self.owned_by.current_line
            and self.compile_options.create_sourcemap
        ):
            returnable.add_stack_initator(
                self.owned_by.current_line, self.owned_by.line_2
            )

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
            PreLine(
                the_command, self.current_line.number, self.current_line.file_index
            ),
            arguments,
            code_block,
        )

    @staticmethod
    def get_stacktrace(
        stack_pile: list[Stack], limit: int = -1
    ) -> list[StackTraceNode]:
        """
        Gets the stack trace from
        the entire stack pile.
        """
        start_index = (
            0 if limit == -1 or len(stack_pile) <= limit else len(stack_pile) - limit
        )
        stacktrace: list[StackTraceNode] = [
            stack_pile[i].return_stack() for i in range(start_index, len(stack_pile))
        ]
        return stacktrace

    def dump_stacktrace(self, limit: int = -1) -> list[StackTraceNode]:
        """
        Return the stack trace from the
        stack pile according to the limit
        given.
        """
        return self.get_stacktrace(self.stack_pile, limit)

    def return_stack(self) -> StackTraceNode:
        """
        Return this stack's traceback
        """
        if not self.current_line:
            raise Exception(
                "Unkown error has occurred: stack has no obvious current line."
            )  # Hopefully not possible
        return StackTraceNode(self.file, self.current_line, self.line_2)

    def add_stack_above(
        self,
        commands: list[PreLine | list],
        file: str | Path | None = None,
        parallel_env: bool = False,
    ):
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
            None,
            parallel_env,
            self.std_out,
        )
        self.owned_stack.env.append_env(self.env)
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

    def make_not_exist_warn(self):
        self.warnings.append(
            f"The command on line {self.current_line.number} may not exist"
            if self.current_line is not None
            else "A command may not exist (unknown line num)",
            self.dump_stacktrace(),
        )

    def __enter__(self):
        return self

    def __exit__(
        self, exception_type: Exception, exception_value: str, exception_traceback: str
    ):
        if self.owned_by and exception_type is None:
            if not self.parallel:
                self.owned_by.env.update_from_env(self.env)
            else:
                self.owned_by.env.append_env(self.env)

            self.owned_by.remove_stack_above()
        return False

    def __iter__(self):
        return self.stack_pile.__iter__()
