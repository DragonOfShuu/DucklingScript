from .token import Token
from typing import Any
from abc import abstractmethod
from ...errors import InvalidArguments


class Operator(Token):
    operators = []
    precedence = []

    def __init__(self, stack: Any):
        self.keywords = self.operators
        super().__init__(stack)

    def init_token_vars(self):
        self.left: Token | None = None
        self.right: Token | None = None
        self.tree_set: bool = False

    def set_left(self, value: Token):
        self.left = value

    def set_right(self, value: Token):
        self.right = value

    def set_tree(self, left: Token, right: Token):
        self.set_left(left)
        self.set_right(right)
        self.tree_set = True

    def solve(self):
        if (not self.left) or (not self.right):
            raise InvalidArguments(
                self.stack,
                """Left node and/or right node were not initialized 
                on parse tree creation. This error cannot and should 
                not occur under any circumstances""",
            )
        return self.solve_operand(self.left.solve(), self.right.solve())

    @abstractmethod
    def solve_operand(self, left: Any, right: Any) -> Any:
        return None
