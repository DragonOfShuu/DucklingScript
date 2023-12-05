from .token import Token
from ...errors import ExpectedTokenError


class String(Token):
    def init_token_vars(self):
        self.isInString = False
        self.closed = False
        self.value: str = ""

    def set_value(self, value: str):
        self.value = value

    def addCharToToken(self, char: str) -> Token.isToken:
        if char != '"' and self.isInString:
            return self.isToken.TRUE

        elif self.isInString:  # char == '"'
            self.isInString = False
            self.closed = True
            return self.isToken.FALSE_SKIP

        elif char == '"':  # and not self.isinstring
            self.isInString = True
            return self.isToken.TRUE_CONTINUE

        return self.isToken.FALSE

    def not_closed(self):
        raise ExpectedTokenError(self.stack, 'Expected a closing "')
