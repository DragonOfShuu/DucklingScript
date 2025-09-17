from typing import Any

from ...errors import MismatchError
from ..token_value_types import TokenValueTypes
from .operator import Operator


class ConditionalOperator(Operator):
    operators = ["==", "!=", "<", ">", "<=", ">="]
    precedence = [["==", "!=", "<", ">", "<=", ">="]]

    def solve_operand(self, left: Any, right: Any) -> TokenValueTypes:
        try:
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
        except TypeError:
            raise MismatchError(
                self.stack,
                f'Cannot compare values "{type(left).__name__}" and "{type(right).__name__}", as they are different or incompatible types.',
            )
