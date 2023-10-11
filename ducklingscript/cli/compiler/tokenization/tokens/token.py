from __future__ import annotations
from enum import Enum
from typing import Any
from abc import ABC, abstractmethod
from ...errors import ExpectedToken


class Token(ABC):
    class isToken(Enum):
        FALSE = 0  # Stop giving chars, and ask someone else about this char
        TRUE = 1  # Continue giving us chars
        CONTINUE = 2  # After this char you gave me switch to someone else
        RESET_CONTINUE = (
            3  # Start back to the beginning of the token, and check other possibilities
        )
        TRUE_CONTINUE = 4  # Don't use this character, but continue

    def __init__(self, stack: Any):
        self.stack = stack
        self.value: Any
        self.closed: bool = True
        self.__init_token_vars()

    @abstractmethod
    def set_value(self, value: str):
        self.value = value

    @abstractmethod
    def __init_token_vars(self):
        pass

    @abstractmethod
    def addCharToToken(self, char: str) -> Token.isToken:
        """
        Return False if this char
        is not relative to this
        token type.
        """
        return self.isToken.FALSE

    @abstractmethod
    def not_closed(self):
        raise ExpectedToken(self.stack, "Expected a closing character.")

    def solve(self):
        return self.value
