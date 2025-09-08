from .token import Token


class Variable(Token):
    acceptable_vars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
    unacceptable_first_chars = "1234567890"

    def add_char_to_token(self, char: str) -> Token.IsToken:
        if self.first_char:
            if char in self.unacceptable_first_chars:
                return Token.IsToken.RESET_CONTINUE
            self.first_char = False

        if char in self.acceptable_vars:
            return Token.IsToken.TRUE
        else:
            return Token.IsToken.FALSE

    def init_token_vars(self):
        if self.env is not None:
            self.vars = self.env.var.all_vars
        else:
            self.vars = {}
        self.first_char = True

    def set_value(self, value: str):
        potential_value = self.vars.get(value)
        if potential_value is not None:
            self.value = potential_value.value
            return self.value

        raise ValueError(
            f"String {value} was recognized as a variable, but was not one."
        )
