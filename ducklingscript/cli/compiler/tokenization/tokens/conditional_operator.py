from .operator import Operator
from .token import Token


class ConditionalOperator(Operator):
    operators = ["==", "!=", "<", ">", "<=", ">="]
    precedence = [["==", "!=", "<", ">", "<=", ">="]]

    def __init_token_vars(self):
        self.pos_oper = ""

    def __find_operator(self, findable: str) -> bool:
        for i in self.operators:
            if i.startswith(findable):
                return True
        return False

    def addCharToToken(self, char: str) -> Token.isToken:
        found = self.__find_operator(self.pos_oper + char)
        if not self.pos_oper and not found:
            return Token.isToken.FALSE

        elif not self.pos_oper:  # operator found
            self.pos_oper += char
            return Token.isToken.TRUE  # Parse another char

        elif not found:  # char_count true
            if self.pos_oper in self.operators:
                return (
                    Token.isToken.FALSE
                )  # Current char is not this operator, but previous one was
            else:
                return (
                    Token.isToken.RESET_CONTINUE
                )  # Nothing matches up, it is not this operand

        else:  # self.pos_oper and found
            # Max operand size is 2, so if found
            # and we already had a char, then this is is valid
            return Token.isToken.CONTINUE
