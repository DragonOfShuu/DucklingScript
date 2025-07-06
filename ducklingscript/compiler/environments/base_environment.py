from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .env_extend_type import EnvExtendType

if TYPE_CHECKING:
    from ..stack import Stack


class BaseEnvironment(ABC):
    """
    A base class for resource managers.
    """

    @abstractmethod
    def extend_env(
        self,
        stack: "Stack | None",
        owning_env: BaseEnvironment | None,
        extend_type: EnvExtendType,
    ) -> BaseEnvironment:
        """
        Extend the environment to a parallel
        environment if parallel is True.
        """
        ...
