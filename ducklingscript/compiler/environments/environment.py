from __future__ import annotations

from .project_environment import ProjectEnvironment
from .variable_environment import VariableEnvironment
from .base_environment import BaseEnvironment

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..stack import Stack


class Environment(BaseEnvironment):
    """
    Stores and manages both thet
    project env and the variable
    env.
    """

    def __init__(
        self,
        variable_env: VariableEnvironment | None = None,
        project_env: ProjectEnvironment | None = None,
        stack: "Stack|None" = None,
    ):
        self.var = (
            variable_env
            if variable_env is not None
            else VariableEnvironment(stack=stack)
        )
        self.proj = project_env if project_env is not None else ProjectEnvironment()
        self.stack = stack

    @property
    def stack(self):
        return self._stack

    @stack.setter
    def stack(self, value: "Stack|None"):
        self._stack = value
        self.var.stack = value
        return self._stack

    def update_from_env(self, x: Environment):
        self.var.update_from_env(x.var)
        self.proj.update_from_env(x.proj)

    def append_env(self, x: Environment):
        self.var.append_env(x.var)
        self.proj.append_env(x.proj)
