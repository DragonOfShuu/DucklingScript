from __future__ import annotations

from ducklingscript.compiler.environments.env_extend_type import EnvExtendType

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
        extend_type: EnvExtendType | None = None,
    ):
        if extend_type is None:
            self.var = (
                variable_env
                if variable_env is not None
                else VariableEnvironment(stack=stack)
            )
            self.proj = project_env if project_env is not None else ProjectEnvironment()
            self.output = output_env if output_env is not None else OutputEnvironment()
            self.stack = stack
            return

        if not variable_env or not project_env or not output_env:
            raise ValueError(
                "When extend_type is set, variable_env, project_env, and output_env must be provided."
            )

        self.var = variable_env.extend_env(stack, self, extend_type)
        self.proj = project_env.extend_env(stack, self, extend_type)
        self.output = output_env.extend_env(stack, self, extend_type)
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

    def extend_env(
        self,
        stack: "Stack | None",
        owning_env: BaseEnvironment | None,
        extend_type: EnvExtendType,
    ) -> Environment:
        """
        Extend the environment to a parallel
        environment if parallel is True.
        """
        # new_var_env = self.var.extend_env(stack, self, extend_type)
        # new_proj_env = self.proj.extend_env(stack, self, extend_type)
        # new_output_env = self.output.extend_env(stack, self, extend_type)

        return Environment(
            stack=stack,
            variable_env=self.var,
            project_env=self.proj,
            output_env=self.output,
            extend_type=extend_type,
        )
