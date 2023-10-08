from typing import Any
from .token import Token

class String(Token):
    def __init_token_vars(self):
        self.isInString = False
        self.value = ""

    def addCharToToken(self, char: str) -> Token.isToken:
        if char != '"' and self.isInString: 
            self.value += char
            return self.isToken.TRUE
        
        elif char=='"' and self.isInString:
            self.isInString = False
            return self.isToken.CONTINUE
        
        elif char=='"': # and not self.isinstring
            self.isInString = True
            return self.isToken.TRUE
        
        return self.isToken.FALSE
    