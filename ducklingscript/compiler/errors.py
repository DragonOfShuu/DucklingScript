from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .pre_line import PreLine


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
    def __init__(self, stack: Any | None, *args: object) -> None:
        super().__init__(*args)
        if (stack is not None) and (not hasattr(stack, "get_stacktrace")):
            raise AttributeError("Stack given is required to be of type stack.")
        self.stack = stack

    def stack_traceback(self, limit: int = -1) -> list[StackTraceNode]:
        if self.stack is None:
            return []

        return self.stack.dump_stacktrace(limit)


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
