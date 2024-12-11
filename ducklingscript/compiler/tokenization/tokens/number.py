from ...errors import ExpectedTokenError
from typing_extensions import override
from .token import Token


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

    def add_char_to_token(self, char: str) -> Token.IsToken:
        self.index += 1

        if char.isnumeric():
            self.closed = True
            return Token.IsToken.TRUE

        if self.index == 0 and char == "-":
            self.is_neg = True
            self.closed = False
            return Token.IsToken.TRUE
        elif char == "." and not self.is_floating_point:
            if self.index == 0:
                self.closed = False
            self.is_floating_point = True
            return Token.IsToken.TRUE

        if self.is_neg and self.index == 1:
            return Token.IsToken.RESET_CONTINUE

        return Token.IsToken.FALSE

    def not_closed(self):
        raise ExpectedTokenError(
            self.stack, "Expected a number, not a lonely dash/period."
        )
