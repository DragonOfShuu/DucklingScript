from typing_extensions import override
from .token import Token
from ...errors import UnexpectedToken

class Number(Token):
    @override
    def __init_token_vars(self):
        self.is_floating_point = False
    
    def addCharToToken(self, char: str) -> Token.isToken:
        if char.isnumeric():
            return Token.isToken.TRUE

        elif char == "." and not self.is_floating_point:
            self.is_floating_point = True
            return Token.isToken.TRUE
        
        elif char == "." and self.is_floating_point:
            raise UnexpectedToken(self.stack, "Unexpected period on this line.")
        
        return Token.isToken.FALSE