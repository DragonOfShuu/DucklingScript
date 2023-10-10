from typing import Literal, Type
from ..errors import UnexpectedToken, ExpectedToken

from .tokens import Token, value_types, operands, isToken, Operator

from dataclasses import dataclass

allowed_types = Literal["str"] | Literal["number"] | Literal["expression"] | None

@dataclass
class SolveData:
    start_index: int
    index: int
    token: Token|None
    string: str = ""

    def reset(self):
        self.string = ""

class ExprTokenizer(Token):
    """
    An expression tokenizer
    """


    def __init_token_vars(self):
        self.depth = 0
        self.value_types = value_types
        self.value_types.append(ExprTokenizer)
        self.operands = operands

    # Break it into a list, so that
    # each value is an even index,
    # and each operation is an odd
    # index.

    # acceptable_str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
    math_operators = ["+", "-", "*", "/", "%"]

    conditional_operators = ["==", "<", ">", "<=", ">=", "and", "or"]

    def set_value(self, value: str):
        if value.startswith("("): 
            value = value[1:]
        if value.startswith(")"):
            value = value[:-1]
        
        self.value = "".join(value.split())

    def addCharToToken(self, char: str) -> Token.isToken:
        if char not in "()" and self.depth:
            return self.isToken.TRUE

        elif self.depth: # char in "()"
            self.depth += 1 if char=="(" else -1

        if self.depth<0:
            raise UnexpectedToken(self.stack, "There is an extra opening parenthesis '('")
        
        elif self.depth>0: # there are parenthesis
            return self.isToken.TRUE

        # If we are of depth 0
        return self.isToken.CONTINUE

    def not_closed(self):
        raise ExpectedToken(self.stack, "Expected a closing parenthesis")
    
    def __resolve_token_return(self, obj: SolveData, returned: isToken, new_char: str):
        match (returned):
            case isToken.FALSE:
                return False
            case isToken.TRUE:
                obj.string+=new_char
                return True
            case isToken.CONTINUE:
                obj.
    
    def solve(self):
        index = 0
        is_operation = False
        current_object: None|SolveData = None
        while index < len(self.value):
            char = self.value[index]

            if current_object is None:
                if is_operation:
                    for i in self.operands:
                        # index, i(self.stack)
                        # current_object = SolveData(index, index, i(self.stack))
                        returned: isToken = current_object.token.addCharToToken(char)

