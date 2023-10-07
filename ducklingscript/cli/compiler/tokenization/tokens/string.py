from .token import Token

class String(Token):
    def __init__(self):
        self.isInString = False
        self.value = ""

    def addCharToToken(self, char: str) -> bool:
        if char != '"' and self.isInString: 
            self.value += char
            return True
        
        elif self.isInString:
            self.isInString = False
            # return False
        
        elif char=='"': # and not self.isinstring
            self.isInString = True
            return True
        
        return False