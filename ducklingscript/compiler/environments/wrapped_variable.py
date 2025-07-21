from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from ..tokenization.token_value_types import TokenValueTypes
from .function_type import Function


if TYPE_CHECKING:
    from .environment import Environment


T = TypeVar("T", TokenValueTypes, Function)


class WrappedVariable(Generic[T]):
    """
    A base class for wrapped data types
    """

    def __init__(self, environment: "Environment", value: T):
        self.environment = environment
        self._value = value

    @property
    def value(self) -> T:
        """
        Get the value of the wrapped data.
        This method should be implemented by subclasses.
        """
        return self._value

    @value.setter
    def value(self, new_value: T):
        """
        Set the value of the wrapped data.
        This method should be implemented by subclasses.
        """
        self._value = new_value
