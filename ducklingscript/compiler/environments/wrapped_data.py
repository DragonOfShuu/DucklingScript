from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar, cast
from enum import Enum

from .function_object import Function


if TYPE_CHECKING:
    from .environment import Environment


class WrappedDataType(Enum):
    USER_VAR = "user_var"
    FUNCTION = "function"


T = TypeVar("T", Function, str, int, float, bool, None)


class WrappedData(Generic[T]):
    """
    A base class for wrapped data types
    """

    def __init__(
        self, environment: "Environment", value_type: WrappedDataType, value: T
    ):
        self.environment = environment
        self.value_type = value_type
        self._value = value

    @property
    def value(self) -> T:
        """
        Get the value of the wrapped data.
        This method should be implemented by subclasses.
        """
        return cast(T, self._value)
