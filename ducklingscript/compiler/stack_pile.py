from pathlib import Path
from typing import TYPE_CHECKING

from .stack import Stack
from .pre_line import PreLine
from .environments.environment import Environment
from .errors import StackOverflowError, StackTraceNode
from .compiled_ducky import CompiledDucky, StackReturnType

if TYPE_CHECKING:
    from .environments.env_extend_type import EnvExtendType

class StackPile:
    def __init__(
        self,
        duckling: list[PreLine | list],
        file: Path | None = None,
        root_env: Environment | None = None,
    ):
        self.duckling = duckling

        self.file = file
        if file and not file.is_file():
            raise TypeError("File given to Stack is required to be a file.")
        self.root_env = root_env if root_env is not None else Environment()

        self.stack_pile: list[Stack] = []
        self.compile_options = self.root_env.proj.compile_options


    def start(self) -> CompiledDucky:
        available_commands = self.root_env.proj.plugin_bus.collect_commands()
        for i in available_commands:
            i.initialize(self, self.root_env)

        base_stack = Stack(self.duckling, self, self.file, None, self.root_env)
        self.stack_pile.append(base_stack)
        compiled = base_stack.run()

        if not (
            compiled.return_type == StackReturnType.NORMAL
            or compiled.return_type == StackReturnType.RETURN
        ):
            self.root_env.output.add_warning(
                f"Program was exited using {compiled.return_type.name} instead of using RETURN"
            )

        return compiled
    
    def dump_stacktrace(
        self, limit: int = -1
    ) -> list[StackTraceNode]:
        """
        Return the stack trace from the
        stack pile according to the limit
        given.
        """
        stack_pile = self.stack_pile

        start_index = (
            0 if limit == -1 or len(stack_pile) <= limit else len(stack_pile) - limit
        )

        stacktrace: list[StackTraceNode] = [
            stack_pile[i].return_stack() for i in range(start_index, len(stack_pile))
        ]

        return stacktrace

    def add_stack_above(
        self,
        commands: list[PreLine | list],
        file: str | Path | None = None,
        env_extend_type: EnvExtendType = EnvExtendType.NORMAL,
        injectable_env: Environment | None = None
    ):
        """
        Add a new owned stack
        onto the stack pile.
        """
        if len(self.stack_pile) >= self.compile_options.stack_limit:
            raise StackOverflowError(
                self,
                f"Max stack count was exceeded. (Stack Limit: {self.compile_options.stack_limit})",
            )
        
        latest_stack = self.stack_pile[-1]

        # WE NEED TO TURN THE ENVIRONMENT INTO SOMETHING THAT
        # CAN EASILY BE EXTENDED BY A FUNCTION CALL.
        # YOU'LL BE ABLE TO DO A PARALLEL ENVIRONMENT OR 
        # A SEQUENTIAL ENVIRONMENT.

        # WE COULD DO THIS BY HAVING YOU PASS A "PARALLEL" BOOL
        # AND THE CURRENT ENVIRONMENT TO STACK. STACK COULD THEN
        # USE THE EASY FUNCTION CALL, AND GIVE ITSELF INTO THE 
        # FUNCTION CALL.

        new_stack = Stack(
            commands,
            self,
            file if isinstance(file, Path) else Path(file) if file else None,
            latest_stack if self.stack_pile else None,
            injectable_env if injectable_env else latest_stack.env,
            env_extend_type
        )

        return new_stack


    def remove_stack(self, stack: Stack):
        """
        Remove the stacks above this
        one. This function should
        only have to destroy one stack
        in total; if it has to destroy
        more, you are doing it wrong.
        """
        if not self.stack_pile:
            raise ValueError("Cannot remove stack from an empty stack pile.")

        # Verify stack received is the last one
        if self.stack_pile[-1] != stack:
            raise ValueError(
                "The stack to remove is not the last stack in the pile."
            )
        
        # Remove the stack from the pile
        self.stack_pile.pop()

    
    def __iter__(self):
        return self.stack_pile.__iter__()