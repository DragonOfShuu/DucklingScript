from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..stack import Stack

class BaseEnvironment(ABC):
    """
    A base class for resource managers.
    """

    # @abstractmethod
    # def append_env(self, x: BaseEnvironment):
    #     """
    #     Overwrite self variables
    #     with the environment given.
    #     This *will* add new variables.
    #     """
    #     pass

    # @abstractmethod
    # def update_from_env(self, x: BaseEnvironment):
    #     """
    #     Overwrite self variables
    #     with the environment given.
    #     Does not add new variables.
    #     """
    #     pass
    
    @abstractmethod
    def extend_env(self, stack: "Stack", parallel: bool = False) -> BaseEnvironment:
        """
        Extend the environment to a parallel
        environment if parallel is True.
        """
        ...
