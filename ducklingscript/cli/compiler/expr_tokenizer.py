from typing import Any, Literal
from .stack import Stack
from .errors import ExpectedToken, UnexpectedToken, UnclosedQuotations

allowed_types = Literal["str"] | Literal["number"] | Literal["expression"] | None

# class Number:
#     def __init__(self) -> None:
#         self.number = number

# class String:
#     def __init__(self, string: str):
#         self.string = string


# class Operator:
#     def __init__(self, operator: str) -> None:
#         self.operator = operator
class Token:
    def __init__(
        self,
        value: Any,
    ) -> None:
        self.value = value


# class Operation:
#     def __init__(self, value1: Token, operator: Token, value2: Token) -> None:
#         self.value1 = value1
#         self.operator = operator
#         self.value2 = value2


class Operation:
    def __init__(self, value1: Any, value2: Any, operation: Token):
        self.value1 = value1
        self.value2 = value2
        self.operation = operation

    def solve(self):
        pass


class ExprTokenizer:
    """
    An expression tokenizer
    """

    def __init__(self, expr: str, stack: Stack) -> None:
        self.expr = expr
        self.stack = stack
        self.__parse()

    # Break it into a list, so that
    # each value is an even index,
    # and each operation is an odd
    # index.

    # acceptable_str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
    math_operators = ["+", "-", "*", "/", "%"]

    conditional_operators = ["==", "<", ">", "<=", ">=", "and", "or"]

    def __parse(self):
        expr: list[object] = ["".join(self.expr)]
        expr = self.__parse_string(expr)
        expr = self.__parse_paren(expr)

    def __parse_string(self, text: list[object]):
        returnable: list[object] = []
        for part in text:
            if not isinstance(part, str):
                continue
            pre_string = ""
            string = ""
            in_string = False
            for i in part:
                if not in_string and i != '"':
                    pre_string += i
                    continue

                elif in_string:
                    if not i == '"':
                        string += i
                        continue

                    returnable.append(string)
                    string = ""
                    in_string = False
                    continue

                elif i == '"':
                    if pre_string:
                        returnable.append(pre_string)
                        pre_string = ""

                    in_string = True
            if string:
                raise ExpectedToken(self.stack, "Expected a closing quotation.")
            if pre_string:
                returnable.append(pre_string)
        return returnable

    def __parse_paren(self, text: list[object]):
        returnable: list[object] = []
        for part in text:
            if not isinstance(part, str):
                returnable.append(part)
                continue
            pre_paren = ""
            expr = ""
            open_paren = 0
            for i in part:
                if not open_paren and i != "(":
                    pre_paren += i
                    continue

                if i == ")":
                    open_paren -= 1
                    if open_paren < 0:
                        raise UnexpectedToken(
                            self.stack, "There is an unexpected closing parenthesis."
                        )
                    elif open_paren:
                        expr += i
                        continue
                    returnable.append(ExprTokenizer(expr, self.stack))
                    expr = ""
                    continue

                elif i == "(":
                    open_paren += 1
                    if open_paren:
                        expr += i
                        continue

                    if pre_paren:
                        returnable.append(pre_paren)
                        pre_paren = ""

                expr += i
            if expr:
                raise ExpectedToken(
                    self.stack, "Expected a closing parenthesis on this line."
                )
            if pre_paren:
                returnable.append(pre_paren)
        return returnable

    def solve(self):
        pass

    # @staticmethod
    # def tokenize(expr: str):
    #     pass

    # @staticmethod
    # def validate_syntax(expr: str):
    #     expr = expr.strip()

    #     for i in expr:
    #         pass


# class Parenthesis
