from typing_extensions import override
from .token import Token
from ...errors import ExpectedTokenError


class Number(Token):
    @override
    def init_token_vars(self):
        self.is_floating_point = False
        self.value: int | float
        self.index = -1
        self.is_neg = False

    def set_value(self, value: str):
        if value.isdigit():
            self.value = int(value)
        elif value.endswith("."):
            self.value = int(value.removesuffix("."))
        else:
            self.value = float(value)

        return self.value

    def addCharToToken(self, char: str) -> Token.isToken:
        self.index += 1

        if char.isnumeric():
            self.closed = True
            return Token.isToken.TRUE

        if self.index == 0 and char == "-":
            self.is_neg = True
            self.closed = False
            return Token.isToken.TRUE
        elif char == "." and not self.is_floating_point:
            if self.index == 0:
                self.closed = False
            self.is_floating_point = True
            return Token.isToken.TRUE

        if self.is_neg and self.index == 1:
            return Token.isToken.RESET_CONTINUE

        return Token.isToken.FALSE

    def not_closed(self):
        raise ExpectedTokenError(
            self.stack, "Expected a number, not a lonely dash/period."
        )
