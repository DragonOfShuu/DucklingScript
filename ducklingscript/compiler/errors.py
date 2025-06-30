from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TYPE_CHECKING

from .pre_line import PreLine

if TYPE_CHECKING:
    from .stack_pile import StackPile


class DucklingScriptError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidTabError(DucklingScriptError):
    pass


class UnclosedQuotationsError(DucklingScriptError):
    pass


class InvalidSourceMapError(DucklingScriptError):
    pass


@dataclass
class StackTraceNode:
    file: Path | None
    line: PreLine
    line_2: PreLine | None


class CompilationError(DucklingScriptError):
    def __init__(self, stack_or_stack_pile: Any | None, *args: object) -> None:
        super().__init__(*args)
        stack_pile: StackPile | None = None

        if stack_or_stack_pile is None:
            return

        if hasattr(stack_or_stack_pile, "stack_pile"):
            stack_pile = stack_or_stack_pile.stack_pile

        if hasattr(stack_or_stack_pile, "dump_stacktrace"):
            stack_pile = stack_or_stack_pile

        if stack_pile is None:
            raise AttributeError("Stack given is required to be of type stack.")

        self.stack_pile = stack_pile

    def stack_traceback(self, limit: int = -1) -> list[StackTraceNode]:
        if self.stack_pile is None:
            return []

        return self.stack_pile.dump_stacktrace(limit)


class StackOverflowError(CompilationError):
    pass


class VarIsNonExistentError(CompilationError):
    pass


class UnacceptableVarNameError(CompilationError):
    pass


class InvalidArgumentsError(CompilationError):
    pass


class UnexpectedTokenError(CompilationError):
    pass


class ExpectedTokenError(CompilationError):
    pass


class MismatchError(CompilationError):
    pass


class NotAValidCommandError(CompilationError):
    pass


class CircularStructureError(CompilationError):
    pass


class ExceededLimitError(CompilationError):
    pass


class InvalidCommandError(CompilationError):
    pass


class StackReturnTypeError(CompilationError):
    pass


class NoKeyToReleaseError(CompilationError):
    pass


class DivideByZeroError(CompilationError):
    def __init__(self, stack: Any | None) -> None:
        super().__init__(
            stack,
            "You cannot divide by zero. (Yes, even computers cannot divide by zero; crazy right?)",
        )


class WarningsObject(list):
    class CustomWarning:
        def __init__(self, error: str, stacktrace: list[StackTraceNode] | None = None):
            self.error = error
            self.stacktrace = stacktrace

    def __init__(self, start_with_warnings: list[CustomWarning] | None = None):
        if start_with_warnings is None:
            start_with_warnings = []
        super().__init__(start_with_warnings)

    def append(self, warning: str, stacktrace: list[StackTraceNode] | None = None):
        if (warning, stacktrace) not in self:
            super().append(self.CustomWarning(warning, stacktrace))

    def retrieve_warnings(self):
        return self.copy()

    def __contains__(
        self, item: CustomWarning | tuple[str, list[StackTraceNode] | None]
    ):
        warning: str = ""
        stacktrace: list[StackTraceNode] | None = None
        if isinstance(item, self.CustomWarning):
            warning = item.error
            stacktrace = item.stacktrace
        else:
            warning = item[0]
            stacktrace = item[1]

        for i in self:
            if i.error == warning and i.stacktrace == stacktrace:
                return True
        return False

    def __iter__(self) -> Iterator[CustomWarning]:
        return super().__iter__()
