from .token import Token
from ...errors import ExpectedTokenError


class String(Token):
    def init_token_vars(self):
        self.isInString = False
        self.closed = False
        self.value: str = ""
        self.escaped = False

    def set_value(self, value: str):
        self.value = value

    def add_char_to_token(self, char: str) -> Token.IsToken:
        if self.escaped:
            self.escaped = False
            return self.IsToken.TRUE

        if char == "\\" and self.isInString:
            self.escaped = True
            return self.IsToken.TRUE_CONTINUE

        if char != '"' and self.isInString:
            return self.IsToken.TRUE

        elif self.isInString:  # char == '"'
            self.isInString = False
            self.closed = True
            return self.IsToken.FALSE_SKIP

        elif char == '"':  # and not self.isinstring
            self.isInString = True
            return self.IsToken.TRUE_CONTINUE

        return self.IsToken.FALSE

    def not_closed(self):
        raise ExpectedTokenError(self.stack, 'Expected a closing "')
