from typing import Any
from .operator import Operator
from .token import Token


class ConditionalOperator(Operator):
    operators = ["==", "!=", "<", ">", "<=", ">="]
    precedence = [["==", "!=", "<", ">", "<=", ">="]]

    def __find_operator(self, findable: str) -> bool:
        for i in self.operators:
            if i.startswith(findable):
                return True
        return False

    def solve_operand(self, left: Any, right: Any) -> Any:
        # return super().solve_operand(left, right)
        match (self.value):
            case "==":
                return left == right
            case _:
                return left == right
