from .token import Token
from ...errors import UnexpectedTokenError


class Boolean(Token):
    keywords = ["TRUE", "FALSE"]

    def init_token_vars(self):
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
