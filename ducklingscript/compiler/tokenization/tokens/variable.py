from ...errors import VarIsNonExistentError
from .token import Token


class Variable(Token):
    acceptable_vars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
    unacceptable_first_chars = "1234567890."

    def add_char_to_token(self, char: str) -> Token.IsToken:
        if self.first_char:
            if char.isspace(): # In case there is a space after the dot
                return Token.IsToken.TRUE_CONTINUE
            if char in self.unacceptable_first_chars:
                return Token.IsToken.RESET_CONTINUE
            
            self.first_char = False

        if char == ".":
            self.first_char = True
            return Token.IsToken.TRUE

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
        parts = value.split(".")
        lookin_location = self.vars

        for name in parts:
            potential_value = lookin_location.get(name)
            if potential_value is None:
                raise VarIsNonExistentError(f"Variable '{value}' is not defined in the current environment.")
            
            if not isinstance(potential_value, dict):
                if name != parts[-1]:
                    raise VarIsNonExistentError(f"Variable '{parts[parts.index(name)+1]}' is not an extension of {name}.")
                
                self.value = potential_value.value
                return self.value

            lookin_location = potential_value

        # self.value = str(lookin_location)
        # return self.value
        self.value = lookin_location
        return self.value