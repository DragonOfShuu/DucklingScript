from typing import Any


class CompilationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidTab(CompilationError):
    pass


class StackableError(CompilationError):
    def __init__(self, stack: Any, *args: object) -> None:
        super().__init__(*args)
        if not hasattr(stack, "get_stacktrace"):
            raise AttributeError("Stack given is required to be of type stack.")
        self.stack = stack

    def stack_traceback(self, limit: int = -1) -> list[str]:
        return self.stack.dump_stacktrace(limit)


class StackOverflowError(StackableError):
    pass


class VarIsNonExistent(StackableError):
    pass


class InvalidArguments(StackableError):
    pass


class WarningsObject:
    class CustomWarning:
        def __init__(self, error: str, stacktrace: list[str] | None = None):
            self.error = error
            self.stacktrace = stacktrace

    def __init__(self, start_with_warnings: list[CustomWarning] = []):
        self.warnings = start_with_warnings

    def append(self, warning: str, stacktrace: list[str] | None = None):
        self.warnings.append(self.CustomWarning(warning, stacktrace))

    def retrieve_warnings(self, include_stacktrace: bool = True):
        returnable = []
        for warning, trace in self:
            addable = []
            if include_stacktrace and trace:
                addable.extend(trace)
            addable.append(warning)
            returnable.append(addable)
        return returnable

    def __iter__(self):
        for x in self.warnings:
            yield (x.error, x.stacktrace)