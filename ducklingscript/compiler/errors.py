from typing import Any


class CompilationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidTab(CompilationError):
    pass


class UnclosedQuotations(CompilationError):
    pass


class StackableError(CompilationError):
    def __init__(self, stack: Any | None, *args: object) -> None:
        super().__init__(*args)
        if (stack is not None) and (not hasattr(stack, "get_stacktrace")):
            raise AttributeError("Stack given is required to be of type stack.")
        self.stack = stack

    def stack_traceback(self, limit: int = -1) -> list[str]:
        if self.stack is None:
            return []

        return self.stack.dump_stacktrace(limit)


class StackOverflowError(StackableError):
    pass


class VarIsNonExistent(StackableError):
    pass


class UnacceptableVarName(StackableError):
    pass


class InvalidArguments(StackableError):
    pass


class UnexpectedToken(StackableError):
    pass


class ExpectedToken(StackableError):
    pass


class MismatchError(StackableError):
    pass


class DivideByZero(StackableError):
    def __init__(self, stack: Any | None) -> None:
        super().__init__(
            stack,
            "You cannot divide by zero. (Yes, even computers cannot divide by zero; crazy right?)",
        )


class WarningsObject(list):
    class CustomWarning:
        def __init__(self, error: str, stacktrace: list[str] | None = None):
            self.error = error
            self.stacktrace = stacktrace

    def __init__(self, start_with_warnings: list[CustomWarning] = []):
        # self.warnings = start_with_warnings
        super().__init__(start_with_warnings)

    def append(self, warning: str, stacktrace: list[str] | None = None):
        if not (warning, stacktrace) in self:
            super().append(self.CustomWarning(warning, stacktrace))

    def retrieve_warnings(self):
        # returnable = []
        # for warning in self:
        #     addable = []
        #     if include_stacktrace and warning.stacktrace:
        #         addable.extend(warning.stacktrace)
        #     addable.append(warning)
        #     returnable.append(addable)
        # return returnable
        return self.copy()

    # def __iter__(self):
    #     return self.warnings.__iter__()

    def __contains__(self, item: CustomWarning | tuple[str, list[str] | None]):
        warning: str = ""
        stacktrace: list[str] | None = None
        if isinstance(item, self.CustomWarning):
            warning = item.error
            stacktrace = item.stacktrace
        else:
            warning, stacktrace = item

        for i in self:
            if i.error == warning and i.stacktrace == stacktrace:
                return True
        return False

    # def __len__(self):
    #     return self.warnings.__len__()
