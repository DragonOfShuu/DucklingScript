from __future__ import annotations
from pathlib import Path
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

from .pre_line import PreLine
from .errors import StackTraceNode
from .commands import BaseCommand, SimpleCommand
from .environments.environment import Environment
from .compile_options import CompileOptions
from .compiled_ducky import StackReturnType, CompiledDucky

if TYPE_CHECKING:
    from .stack_pile import StackPile
    from .environments.env_extend_type import EnvExtendType

@dataclass
class ParsedCommand:
    command_name: PreLine
    argument: str | None = None
    code_block: list[PreLine] | None = None

    def asdict(self):
        return asdict(self)


class Stack:
    """
    A class that compiles code
    within an environment. Creates
    new stacks above this one when
    necessary.

    Args:
        duckling: A list of prelines, or a list of a list of prelines, or a li...
        stack_pile: The stack of stacks
        file: The file that is being ran at
        owned_by: The stack that owns this one.
        env: The environment to run the stack within
        parallel: Whether this stack runs in the same environment as the one below it or not. (functions are not parallel, starting code using STARTENV is (we pull all vars from STARTENV directly into this one))
    """

    def __init__(
        self,
        duckling: list[PreLine | list],
        stack_pile: StackPile,
        file: Path | None = None,
        owned_by: Stack | None = None,
        env: Environment | None = None,
        extend_type: EnvExtendType = EnvExtendType.NORMAL,
    ):
        self.duckling = duckling
        self.stack_pile = stack_pile

        self.current_line: PreLine | None = None
        self.next_line: list[PreLine] | PreLine | None = None
        self.owned_stack: Stack | None = None
        self.owned_by: Stack | None = owned_by
        if file and not file.is_file():
            raise TypeError("File given to Stack is required to be a file.")
        self.file = file
        self.env = env.extend_env(self, extend_type) if env is not None else Environment(stack=self)
        self.extend_type: EnvExtendType = extend_type

        self.line_2: PreLine | None = None
        """
        The secondary line that
        can be defined by an
        inner command. 

        Mainly used for determining
        the location of an error.
        """
        self.return_type: StackReturnType | None = None
        self.compile_options: CompileOptions = self.stack_pile.compile_options

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
            for i in self.env.proj.plugin_bus.collect_commands():
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
            self.env.output.stdout.extend(new_compiled.std_out)

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
    
    def make_not_exist_warn(self):
        self.env.output.add_warning(
            f"The command on line {self.current_line.number} may not exist"
            if self.current_line is not None
            else "A command may not exist (unknown line num)"
        )
    
    def return_stack(self) -> StackTraceNode:
        """
        Return this stack's traceback
        """
        if not self.current_line:
            raise Exception(
                "Unkown error has occurred: stack has no obvious current line."
            )  # Hopefully not possible
        return StackTraceNode(self.file, self.current_line, self.line_2)

    def __enter__(self):
        return self

    def __exit__(
        self, exception_type: Exception, exception_value: str, exception_traceback: str
    ):
        if self.owned_by and exception_type is None:
            if not self.extend_type:
                self.owned_by.env.update_from_env(self.env)
            else:
                self.owned_by.env.append_env(self.env)

            self.stack_pile.remove_stack(self)
            # self.remove_from_stack()
        return False
