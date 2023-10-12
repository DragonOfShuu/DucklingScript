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

    keywords: list[str] = []

    def __init__(self, stack: Any):
        self.stack = stack
        self.value: Any
        self.closed: bool = True

        if self.keywords:
            self.expected_value: list[int] | None = None
            self.index = 0
            self.current_value = ""

        self.init_token_vars()

    # @abstractmethod
    def set_value(self, value: str):
        self.value = value

    # @abstractmethod
    def init_token_vars(self):
        pass

    def parse_for_keywords(self, char: str) -> Token.isToken:
        self.current_value += char
        num_key = range(len(self.keywords))
        listable = self.expected_value if self.expected_value is not None else num_key

        new_expected = [
            i for i in listable if self.keywords[i].startswith(self.current_value)
        ]

        if len(new_expected) == 0:
            return Token.isToken.RESET_CONTINUE

        self.expected_value = new_expected

        if len(new_expected) > 1:
            return Token.isToken.TRUE
        else:  # len(new_expected) == 1
            word = self.keywords[new_expected[0]]
            return (
                Token.isToken.CONTINUE
                if word == self.current_value
                else Token.isToken.TRUE
            )

    def addCharToToken(self, char: str) -> Token.isToken:
        """
        Return False if this char
        is not relative to this
        token type.
        """
        if self.keywords:
            return self.parse_for_keywords(char)
        return self.isToken.FALSE

    # @abstractmethod
    def not_closed(self):
        raise ExpectedToken(self.stack, "Expected a closing character.")

    def solve(self):
        return self.value
