from typing import Any
from .operator import Operator
from .token import Token
from ...errors import MismatchError, UnexpectedToken


class MathOperator(Operator):
    operators = ["+", "-", "*", "/", "%"]

    def addCharToToken(self, char: str) -> Token.isToken:
        if char in self.operators:
            return Token.isToken.CONTINUE
        return Token.isToken.FALSE

    def set_value(self, value: str):
        self.value = value

    def solve_operand(self, left: Any, right: Any) -> Any:
        if self.value=="+":
            if type(left)==str or type(right)==str:
                left = str(left); right = str(right)
            return left+right
        
        if type(left)!=float or type(left)!=int:
            raise MismatchError(f"Operand {self.value} is not supported for type {left}'")

        match (self.value):
            case "-": return left-right
            case "*": return left*right
            case "/": return left/right
            case _:
                return left%right
        