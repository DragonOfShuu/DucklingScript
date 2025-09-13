from __future__ import annotations

from typing import TYPE_CHECKING

from ...tokenization.token_value_types import TokenValueTypes


if TYPE_CHECKING:
    from ..environment import Environment


class WrappedVariable():
    """
    A base class for wrapped data types
    """

    def __init__(self, environment: "Environment", value: TokenValueTypes):
        self.environment = environment
        self._value = value

    @property
    def value(self) -> TokenValueTypes:
        """
        Get the value of the wrapped data.
        This method should be implemented by subclasses.
        """
        return self._value

    @value.setter
    def value(self, new_value: TokenValueTypes):
        """
        Set the value of the wrapped data.
        This method should be implemented by subclasses.
        """
        self._value = new_value
