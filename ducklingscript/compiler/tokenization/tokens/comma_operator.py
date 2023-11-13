from typing import Any
from .operator import Operator


class CommaOperator(Operator):
    operators = [","]
    precedence = [[","]]

    def solve_operand(self, left: Any, right: Any) -> Any:
        if isinstance(left, list):
            return left.append(right)

        return [left, right]
