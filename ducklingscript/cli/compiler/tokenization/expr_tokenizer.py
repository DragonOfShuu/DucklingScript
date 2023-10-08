from typing import Any, Literal
from ..stack import Stack
# from ..errors import ExpectedToken, UnexpectedToken, UnclosedQuotations
from .tokens import Token

allowed_types = Literal["str"] | Literal["number"] | Literal["expression"] | None

# class Operation:
#     def __init__(self, value1: Any, value2: Any, operation: Token):
#         self.value1 = value1
#         self.value2 = value2
#         self.operation = operation

#     def solve(self):
#         pass

class ExprTokenizer:
    """
    An expression tokenizer
    """

    def __init__(self, expr: str, stack: Stack) -> None:
        # if isinstance(expr, str):
        #     expr = ["".join(expr)]
        self.expr = expr
        self.stack = stack
        self.__parse(expr)

    # Break it into a list, so that
    # each value is an even index,
    # and each operation is an odd
    # index.

    # acceptable_str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
    math_operators = ["+", "-", "*", "/", "%"]

    conditional_operators = ["==", "<", ">", "<=", ">=", "and", "or"]

    def __parse(self, expr):
        pass
        # expr = self.__parse_string(expr)
        # expr = self.__parse_paren(expr)

    # def __parse_string(self, text: list[object]) -> list[object]:
    #     returnable: list[object] = []
    #     for i in text:
    #         if not isinstance(i, str):
    #             returnable.append(i)
    #             continue
    #         quotation_points = i.split('"')

    #         if len(quotation_points) % 2 == 0:
    #             raise ExpectedToken(self.stack, "Expected a closing quotation.")

    #         for count, i in enumerate(quotation_points):
    #             if count % 2 == 0 and i == "":
    #                 continue
    #             if count % 2 == 1:
    #                 returnable.append(Token(i))  # Successful String
    #             else:
    #                 returnable.append(i)  # Still unparsed
    #     return returnable

    # def __parse_paren(self, text: list[object]):
    #     returnable: list[object] = []
    #     depth = 0
    #     addable = []
    #     for chunk in text:
    #         depth = self.__parse_paren_chunk(chunk, addable, returnable, depth)

    #     if depth > 0:
    #         raise ExpectedToken(
    #             self.stack, "Expected a closing parenthesis on this line"
    #         )
    #     if addable:
    #         returnable.append(addable)
    #     return returnable

    # def __parse_paren_chunk(
    #     self, chunk: object, addable: list, returnable: list[object], depth: int
    # ) -> int:
    #     if not isinstance(chunk, str):
    #         addable.append(chunk)
    #         return depth

    #     for i in chunk:
    #         if i not in "()":
    #             addable.append(i)

    #         depth += 1 if i == "(" else 0
    #         if depth == 0:
    #             returnable.append(ExprTokenizer(addable, self.stack))
    #             addable = []
    #         elif depth < 0:
    #             raise UnexpectedToken(
    #                 self.stack,
    #                 "Unnecessary openinng parenthesis discovered on this line.",
    #             )
    #         elif depth == 1:
    #             returnable.extend(addable)
    #             addable = []
    #         else:
    #             addable.append(i)
    #     return depth


    def solve(self):
        pass
