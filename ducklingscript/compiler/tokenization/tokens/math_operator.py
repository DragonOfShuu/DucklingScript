from typing import Any
from .operator import Operator
from ...errors import MismatchError, DivideByZeroError


class MathOperator(Operator):
    operators = ["+", "-", "*", "/", "//", "%", "^"]
    precedence = [["^"], ["*", "/", "//", "%"], ["+", "-"]]

    def solve_operand(self, left: Any, right: Any) -> Any:
        if self.value == "+":
            if type(left) == str or type(right) == str:
                left = str(left)
                right = str(right)
            return left + right

        if not (type(left) == float or type(left) == int):
            raise MismatchError(
                self.stack,
                f"Operand {self.value} is not supported for type '{left}' and '{right}'",
            )

        match (self.value):
            case "-":
                return left - right
            case "*":
                return left * right
            case "/":
                if right == 0:
                    raise DivideByZeroError(self.stack)
                return left / right
            case "//":
                return left // right
            case "^":
                return left**right
            case _:
                return left % right
