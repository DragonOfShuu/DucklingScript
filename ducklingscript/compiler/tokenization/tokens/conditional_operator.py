from typing import Any
from .operator import Operator
from .token import Token


class ConditionalOperator(Operator):
    operators = ["==", "!=", "<", ">", "<=", ">="]
    precedence = [["==", "!=", "<", ">", "<=", ">="]]

    def solve_operand(self, left: Any, right: Any) -> Any:
        match (self.value):
            case "==":
                return left == right
            case "!=":
                return left != right
            case "<":
                return left < right
            case ">":
                return left > right
            case "<=":
                return left <= right
            case ">=":
                return left >= right
            case _:
                raise NotImplementedError("Operator not implemented.")
