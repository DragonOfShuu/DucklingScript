from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .pre_line import PreLine


class CompilationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidTabError(CompilationError):
    pass


class UnclosedQuotationsError(CompilationError):
    pass


@dataclass
class StackTraceNode:
    file: Path | None
    line: PreLine
    line_2: PreLine | None


class GeneralError(CompilationError):
    def __init__(self, stack: Any | None, *args: object) -> None:
        super().__init__(*args)
        if (stack is not None) and (not hasattr(stack, "get_stacktrace")):
            raise AttributeError("Stack given is required to be of type stack.")
        self.stack = stack

    def stack_traceback(self, limit: int = -1) -> list[StackTraceNode]:
        if self.stack is None:
            return []

        return self.stack.dump_stacktrace(limit)


class StackOverflowError(GeneralError):
    pass


class VarIsNonExistentError(GeneralError):
    pass


class UnacceptableVarNameError(GeneralError):
    pass


class InvalidArgumentsError(GeneralError):
    pass


class UnexpectedTokenError(GeneralError):
    pass


class ExpectedTokenError(GeneralError):
    pass


class MismatchError(GeneralError):
    pass


class NotAValidCommandError(GeneralError):
    pass


class CircularStructureError(GeneralError):
    pass


class ExceededLimitError(GeneralError):
    pass


class InvalidCommandError(GeneralError):
    pass


class StackReturnTypeError(GeneralError):
    pass


class DivideByZeroError(GeneralError):
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
        # def __contains__(self, item: CustomWarning):
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
