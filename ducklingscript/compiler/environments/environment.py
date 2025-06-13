from __future__ import annotations

from .output_environment import OutputEnvironment
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
        stack: "Stack|None" = None,
        variable_env: VariableEnvironment | None = None,
        project_env: ProjectEnvironment | None = None,
        output_env: OutputEnvironment | None = None,
    ):
        self.var = (
            variable_env
            if variable_env is not None
            else VariableEnvironment(stack=stack)
        )
        self.proj = project_env if project_env is not None else ProjectEnvironment()
        self.output = (
            output_env if output_env is not None else OutputEnvironment()
        )
        self.stack = stack

    @property
    def stack(self):
        return self._stack

    @stack.setter
    def stack(self, value: "Stack|None"):
        self._stack = value
        self.var.stack = value
        self.output.stack = value
        return self._stack

    # def update_from_env(self, x: Environment):
    #     self.var.update_from_env(x.var)
    #     self.proj.update_from_env(x.proj)
    #     self.output.update_from_env(x.output)

    # def append_env(self, x: Environment):
    #     self.var.append_env(x.var)
    #     self.proj.append_env(x.proj)
    #     self.output.append_env(x.output)

    def extend_env(self, stack: "Stack", parallel: bool = False) -> Environment:
        """
        Extend the environment to a parallel
        environment if parallel is True.
        """
        new_var_env = self.var.extend_env(parallel)
        new_proj_env = self.proj.extend_env(parallel)
        new_output_env = self.output.extend_env(parallel)

        return Environment(
            stack=stack,
            variable_env=new_var_env,
            project_env=new_proj_env,
            output_env=new_output_env,
        )
