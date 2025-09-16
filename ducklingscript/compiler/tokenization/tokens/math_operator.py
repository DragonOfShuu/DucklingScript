from ..token_value_types import TokenValueTypes
from .operator import Operator
from ...errors import MismatchError, DivideByZeroError


class MathOperator(Operator):
    operators = ["+", "-", "*", "/", "//", "%", "^"]
    precedence = [["^"], ["*", "/", "//", "%"], ["+", "-"]]

    def solve_operand(
        self, left: TokenValueTypes, right: TokenValueTypes
    ) -> TokenValueTypes:
        if self.value == "+" and (type(left) is str or type(right) is str):
            left = str(left)
            right = str(right)
            return left + right

        if not (type(left) is float or type(left) is int) or not (
            type(right) is float or type(right) is int
        ):
            raise MismatchError(
                self.stack,
                f"Operand {self.value} is not supported for type '{type(left).__name__}' and '{type(right).__name__}'",
            )

        match (self.value):
            case "+":
                return left + right
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
