from __future__ import annotations
from abc import ABC, abstractmethod


class BaseEnvironment(ABC):
    @abstractmethod
    def append_env(self, x: BaseEnvironment):
        """
        Overwrite self variables
        with the environment given.
        This *will* add new variables.
        """
        pass

    @abstractmethod
    def update_from_env(self, x: BaseEnvironment):
        """
        Overwrite self variables
        with the environment given.
        Does not add new variables.
        """
        pass
