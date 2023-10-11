from typing import Literal, Sequence
from ..errors import UnexpectedToken, ExpectedToken

from .tokens import Token, value_types, operands, isToken, Operator

from dataclasses import dataclass, field

allowed_types = Literal["str"] | Literal["number"] | Literal["expression"] | None


@dataclass
class SolveData:
    start_index: int = 0
    index: int = 0
    token: Token | None = None
    is_operation: bool = False
    string: str = ""
    parse_list: list[Token] = field(default_factory=list)
    blacklist: list[type[Token]] = field(default_factory=list)

    def switch_operand(self):
        """
        Adjusts values to switch
        the operand.

        Make sure the index is set to
        the new index before hand, as
        the start index will now equal
        it.
        """
        self.start_index = self.index
        self.token = None
        self.is_operation = not self.is_operation
        self.blacklist = []
        self.string = ""

    def reset(self, reset_blacklist: bool = False):
        """
        Resets the string
        and the index.
        """
        self.index = self.start_index
        self.string = ""
        self.token = None
        if reset_blacklist:
            self.blacklist = []

    def set_token(self, new_token: Token):
        self.token = new_token

    def reset_token(self):
        self.token = None

    def append_and_switch(self):
        if self.token is None:
            raise TypeError("Token is None.")
        self.token.set_value(self.string)
        self.parse_list.append(self.token)
        self.switch_operand()

    def add_blacklist(self, x: type[Token]):
        self.blacklist.append(x)

    def reset_blacklist(self):
        self.blacklist = []


class ExprTokenizer(Token):
    """
    An expression tokenizer
    """

    def __init_token_vars(self):
        self.depth = 0
        self.value_types = value_types
        self.value_types.append(ExprTokenizer)
        self.operands = operands
        self.closed = False

    # Break it into a list, so that
    # each value is an even index,
    # and each operation is an odd
    # index.

    # acceptable_str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
    math_operators = ["+", "-", "*", "/", "%"]

    conditional_operators = ["==", "<", ">", "<=", ">=", "and", "or"]

    def set_value(self, value: str):
        if value.startswith("("):
            value = value[1:]
        if value.startswith(")"):
            value = value[:-1]

        self.value = "".join(value.split())

    def addCharToToken(self, char: str) -> Token.isToken:
        if char not in "()" and self.depth:
            return self.isToken.TRUE

        elif char in "()":
            self.depth += 1 if char == "(" else -1

        if self.depth < 0:
            raise UnexpectedToken(
                self.stack, "There is an extra opening parenthesis '('"
            )

        elif self.depth > 0:  # there are parenthesis
            return self.isToken.TRUE

        # If we are of depth 0
        self.closed = True
        return self.isToken.CONTINUE

    def not_closed(self):
        raise ExpectedToken(self.stack, "Expected a closing parenthesis")

    def __resolve_token_return(
        self,
        obj: SolveData,
        returned: isToken,
        new_char: str,
        false_is_switch_operand: bool = False,
    ):
        match (returned):
            case isToken.FALSE:
                if false_is_switch_operand:
                    obj.append_and_switch()
                else:
                    obj.index += 1
                return False
            case isToken.TRUE:
                obj.string += new_char
                obj.index += 1
                return True
            case isToken.CONTINUE:
                obj.string += new_char
                obj.index += 1
                obj.append_and_switch()
                return True
            case isToken.RESET_CONTINUE:
                if obj.token:
                    obj.add_blacklist(type(obj.token))
                obj.reset()
                return False
            case isToken.TRUE_CONTINUE:
                obj.index += 1
                return True

    def __verify_char(
        self,
        obj: SolveData,
        char: str,
        tokens: Sequence[type[Token]],
        error_message: str,
    ):
        for i in tokens:
            obj.set_token(i(self.stack))
            returned: isToken = obj.token.addCharToToken(  # type:ignore
                char
            )
            breakable = self.__resolve_token_return(obj, returned, char)
            if breakable:
                break
        else:
            raise ExpectedToken(self.stack, error_message)
    
    def __convert_string(self, obj: SolveData):
        to_parse = self.value
        while obj.index < len(to_parse):
            char = to_parse[obj.index]

            if obj.token is None:
                self.__verify_char(
                    obj,
                    char,
                    self.value_types if not obj.is_operation else self.operands,
                    f"A valid {'operand' if obj.is_operation else 'value'} was expected",
                )
                continue

            value = obj.token.addCharToToken(char)
            self.__resolve_token_return(obj, value, char, false_is_switch_operand=True)

        if obj.token and not obj.token.closed:
            obj.token.not_closed()
        if len(obj.parse_list)%2==0:
            raise ExpectedToken("Values are expected after an operator")
    
    def __build_parse_trees(self, obj: SolveData):
        # for i in all operands in the language
        for the_type in self.operands:
            # for i in the precedence of that type of operand
            for i in the_type.precedence:
                index = 0
                while index < len(obj.parse_list):
                    token: Token = obj.parse_list[index]
                    if not isinstance(token, Operator) or token.tree_set or type(token) not in i: 
                        index+=1
                        continue
                    
                    right = obj.parse_list.pop(index+1)
                    left = obj.parse_list.pop(index-1)
                    token.set_tree(left, right)
        if len(obj.parse_list)!=1:
            raise ExpectedToken(self.stack, f"Parsing failed. Size of root was {len(obj.parse_list)}")

    def solve(self) -> str | int | float | bool:
        obj: SolveData = SolveData()
        
        self.__convert_string(obj)

        self.__build_parse_trees(obj)
        
        return obj.parse_list[0].solve()
