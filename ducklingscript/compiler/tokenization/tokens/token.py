from __future__ import annotations
from enum import Enum
from typing import Any
from abc import ABC
from ...errors import ExpectedTokenError
from ...environments.environment import Environment


class Token(ABC):
    class IsToken(Enum):
        FALSE = 0  # Stop giving chars, and ask someone else about this char
        TRUE = 1  # Continue giving us chars
        CONTINUE = 2  # After this char you gave me switch to someone else
        FALSE_SKIP = 3  # Skip this char then switch to someone else
        RESET_CONTINUE = (
            4  # Start back to the beginning of the token, and check other possibilities
        )
        TRUE_CONTINUE = 5  # Don't use this character, but continue

    keywords: list[str] = []

    def __init__(self, stack: Any, env: Environment):
        self.stack = stack
        self.value: Any
        self.closed: bool = True
        self.env = env

        if self.keywords:
            self.init_keyword_vars()

        self.init_token_vars()

    def set_value(self, value: str):
        self.value = value

    def init_token_vars(self):
        pass

    def init_keyword_vars(self):
        self.expected_value: list[int] | None = None
        self.current_value = ""

    def parse_for_keywords(self, char: str) -> Token.IsToken:
        self.current_value += char
        num_key = range(len(self.keywords))
        listable = self.expected_value if self.expected_value is not None else num_key

        new_expected = [
            i for i in listable if self.keywords[i].startswith(self.current_value)
        ]

        if len(new_expected) == 0:
            if self.expected_value is not None:
                for i in self.expected_value:
                    if self.keywords[i] == self.current_value[:-1]:
                        return Token.IsToken.FALSE
            return Token.IsToken.RESET_CONTINUE

        self.expected_value = new_expected

        if len(new_expected) > 1:
            return Token.IsToken.TRUE
        else:  # len(new_expected) == 1
            word = self.keywords[new_expected[0]]
            return (
                Token.IsToken.CONTINUE
                if word == self.current_value
                else Token.IsToken.TRUE
            )

    def add_char_to_token(self, char: str) -> Token.IsToken:
        """
        Return False if this char
        is not relative to this
        token type.
        """
        if self.keywords:
            return self.parse_for_keywords(char)
        return self.IsToken.FALSE

    # @abstractmethod
    def not_closed(self):
        raise ExpectedTokenError(self.stack, "Expected a closing character.")

    def solve(self):
        return self.value
