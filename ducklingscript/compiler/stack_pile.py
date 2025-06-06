from pathlib import Path

from .stack import Stack
from .pre_line import PreLine
from .environments.environment import Environment
from .errors import DucklingScriptError, StackOverflowError, StackTraceNode, WarningsObject
from .compiled_ducky import CompiledDucky, StackReturnType, StdOutData


class StackPile:
    def __init__(
        self,
        duckling: list[PreLine | list],
        file: Path | None = None,
        warnings: WarningsObject | None = None,
        std_out: list[StdOutData] | None = None,
        root_env: Environment | None = None,
    ):
        self.duckling = duckling

        self.file = file
        if file and not file.is_file():
            raise TypeError("File given to Stack is required to be a file.")
        self.warnings = warnings if warnings is not None else WarningsObject()
        self.std_out: list[StdOutData] = [] if std_out is None else std_out
        self.root_env = root_env if root_env is not None else Environment()

        self.stack_pile: list[Stack] = []
        self.compile_options = self.root_env.proj.compile_options


    def start(self) -> CompiledDucky:
        available_commands = self.root_env.proj.plugin_bus.collect_commands()
        for i in available_commands:
            i.initialize(self, self.root_env)

        base_stack = Stack(self.duckling, self, self.file, None, self.root_env, False)
        self.stack_pile.append(base_stack)
        compiled = base_stack.run()

        if not (
            compiled.return_type == StackReturnType.NORMAL
            or compiled.return_type == StackReturnType.RETURN
        ):
            self.warnings.append(
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
        parallel_env: bool = False,
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

        new_stack = Stack(
            commands,
            self,
            file if isinstance(file, Path) else Path(file) if file else None,
            latest_stack if self.stack_pile else None,
            None,
            parallel_env
        )

        # LET'S REWRITE THIS SO WE DON'T HAVE TO
        # CREATE A NEW ENVIRONMENT AND APPEND
        # THE CURRENT ENVIRONMENT
        new_stack.env.append_env(latest_stack.env)
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
            raise DucklingScriptError(
                "The stack to remove is not the last stack in the pile."
            )
        
        # Remove the stack from the pile
        self.stack_pile.pop()


    def add_warning(self, warning: str):
        """
        Add a compiler warning
        """
        self.warnings.append(warning, self.dump_stacktrace())

    
    def __iter__(self):
        return self.stack_pile.__iter__()