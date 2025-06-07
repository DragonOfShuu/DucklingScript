from __future__ import annotations

from typing import TYPE_CHECKING

from ..errors import DucklingScriptError, WarningsObject
from .base_environment import BaseEnvironment

if TYPE_CHECKING:
    from ..stack import Stack
    from ..compiled_ducky import StdOutData

class OutputEnvironment(BaseEnvironment):
    def __init__(
        self,
        stack: Stack | None = None,
        warnings: WarningsObject | None = None,
        stdout: list[StdOutData] | None = None,
    ):
        self.stack = stack
        self.warnings = warnings if warnings is not None else WarningsObject()
        self.stdout = stdout if stdout is not None else []

    @property
    def stack(self) -> Stack:
        if self._stack is None:
            raise DucklingScriptError("Stack is not initialized onto OutputEnvironment.")
        return self._stack

    @stack.setter
    def stack(self, value: Stack | None):
        self._stack = value
        return self._stack

    def add_warning(self, warning: str):
        """
        Add a compiler warning
        """
        self.warnings.append(warning, self.stack.stack_pile.dump_stacktrace())
    
    def add_stdout(self, data: StdOutData):
        self.stdout.append(data)

    def append_env(self, x: OutputEnvironment):
        """
        Overwrite self variables
        with the environment given.
        This *will* add new variables.
        """
        self.warnings.extend(x.warnings)
        self.stdout.extend(x.stdout)

    def update_from_env(self, x: OutputEnvironment):
        """
        Overwrite self variables
        with the environment given.
        Does not add new variables.
        """
        self.warnings.extend(x.warnings)
        self.stdout.extend(x.stdout)
