from .token import Token
from ...errors import UnexpectedToken


class Boolean(Token):
    possible_value = ["TRUE", "FALSE"]

    def __init_token_vars(self):
        self.own_value = ""
        self.index = 0
        self.expected_value = None

    def set_value(self, value: str):
        if value == "TRUE":
            self.value = True
        elif value == "FALSE":
            self.value = False
        else:
            raise TypeError(
                f"Inputted type for type boolean was incorrect (is: {value})"
            )

    def addCharToToken(self, char: str) -> Token.isToken:
        if self.expected_value is None:
            if char != "T" and char != "F":
                return Token.isToken.FALSE

            self.expected_value = char == "T"
            self.index += 1
            return Token.isToken.TRUE

        if self.possible_value[0 if self.expected_value else 1][self.index] == char:
            self.index += 1
            return Token.isToken.TRUE
        else:
            return Token.isToken.FALSE
            # if self.possible_value[1][self.index] == char:
            #     self.index+=1
            #     return Token.isToken.TRUE
