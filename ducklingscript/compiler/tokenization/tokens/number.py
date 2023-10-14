from typing_extensions import override
from .token import Token
from ...errors import UnexpectedToken


class Number(Token):
    @override
    def init_token_vars(self):
        self.is_floating_point = False
        self.value: int | float

    def set_value(self, value: str):
        if value.isdigit():
            self.value = int(value)
        elif value.endswith("."):
            self.value = int(value.removesuffix("."))
        else:
            self.value = float(value)

        return self.value

    def addCharToToken(self, char: str) -> Token.isToken:
        if char.isnumeric():
            return Token.isToken.TRUE

        elif char == "." and not self.is_floating_point:
            self.is_floating_point = True
            return Token.isToken.TRUE

        return Token.isToken.FALSE
