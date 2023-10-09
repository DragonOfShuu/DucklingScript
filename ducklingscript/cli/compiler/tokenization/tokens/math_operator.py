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
        if not type(left)==type(right):
            raise MismatchError(self.stack, "Left and right side of operand must match.")
        
        if self.value=="+":
            return left+right
        elif self.value=="-":
            return left-right
        elif self.value=="*":
            return left*right
        elif self.value=="/":
            return left/right
        else:
            return left%right
        