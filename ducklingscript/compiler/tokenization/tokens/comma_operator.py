from ..token_value_types import TokenValueTypes
from .operator import Operator


class CommaOperator(Operator):
    operators = [","]
    precedence = [[","]]

    def solve_operand(
        self, left: TokenValueTypes, right: TokenValueTypes
    ) -> TokenValueTypes:
        if isinstance(left, list):
            left.append(right)
            return left
        if isinstance(right, list):
            right.insert(0, left)
            return right

        return [left, right]
