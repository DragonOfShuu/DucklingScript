from typing import Any, Literal, Sequence
from ..errors import UnexpectedTokenError, ExpectedTokenError, StackOverflowError
from ..environments.environment import Environment

from .tokens import Token, value_types, operands, IsToken, Operator

from dataclasses import dataclass, field

allowed_types = Literal["str"] | Literal["number"] | Literal["expression"] | None


@dataclass
class SolveData:
    """
    A stateful object containing the
    tokenizers current state on parsing.
    """

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
        """
        Sets the current token
        being used and edited.
        """
        self.token = new_token

    def reset_token(self):
        """
        Sets the current token
        to None
        """
        self.token = None

    def append_and_switch(self):
        """
        Append this token to
        the output, reset
        everything, and switch
        `is_operand`.
        """
        if self.token is None:
            raise TypeError("Token is None.")
        self.token.set_value(self.string)
        self.parse_list.append(self.token)
        self.switch_operand()

    def add_blacklist(self, x: type[Token]):
        """
        Add a new class
        to the blacklist.
        """
        self.blacklist.append(x)

    def reset_blacklist(self):
        """
        Literally reset the
        blacklist.
        """
        self.blacklist = []


token_return_types = str | int | float | bool | list


class Tokenizer(Token):
    """
    An expression evaluator. Converts strings into a
    value by evaluating the expressing contained.

    >>> Tokenizer.tokenize("1 + 1")
    2
    """

    def __init__(
        self, stack: Any | None, env: Environment | None, value: str | None = None
    ):
        if env is None:
            env = Environment()
        super().__init__(stack, env)

        if value is not None:
            self.value: str = value

    def init_token_vars(self):
        """
        Initialize the Tokenizer's
        variables.
        """
        self.depth = 0
        self.ignore_paren = False
        self.value_types = value_types.copy()
        self.value_types.append(Tokenizer)
        self.operands = operands
        self.closed = False
        self.is_opposite = False

    def set_value(self, value: str):
        """
        Set the value for this
        token. Remove extra
        parenthesis if necessary.
        """
        if value.startswith("("):
            value = value[1:]
        if value.endswith(")"):
            value = value[:-1]

        self.value = value

    def add_char_to_token(self, char: str) -> Token.IsToken:
        """
        Attempt to add this
        character to the
        token.
        """
        if (char not in "()" or self.ignore_paren) and self.depth:
            if char == '"':
                self.ignore_paren = not self.ignore_paren
            return self.IsToken.TRUE

        elif char in "()":
            self.depth += 1 if char == "(" else -1

        if self.depth < 0:
            raise UnexpectedTokenError(
                self.stack, "There is an extra opening parenthesis '('"
            )

        elif self.depth > 100:
            raise StackOverflowError(
                self.stack, "Maximum number of parenthesis reached (limit is 100)"
            )

        elif self.depth > 0:  # there are parenthesis
            return self.IsToken.TRUE

        # If we are of depth 0
        if char not in "()":
            if char == "!":
                self.is_opposite = True
                return self.IsToken.TRUE_CONTINUE
            return self.IsToken.RESET_CONTINUE

        self.closed = True
        return self.IsToken.CONTINUE

    def not_closed(self):
        """
        The exception to raise if
        this token was not properly
        closed off.
        """
        raise ExpectedTokenError(self.stack, "Expected a closing parenthesis")

    def __resolve_token_return(
        self,
        obj: SolveData,
        returned: IsToken,
        new_char: str,
        false_is_switch_operand: bool = False,
    ) -> bool:
        """
        This guides the parser on what
        to do depending on what a token
        returns as a value from the char.
        """
        match (returned):
            case IsToken.FALSE:
                if false_is_switch_operand:
                    obj.append_and_switch()
                # else:
                #     obj.index += 1
                return False
            case IsToken.TRUE:
                obj.string += new_char
                obj.index += 1
                return True
            case IsToken.CONTINUE:
                obj.string += new_char
                obj.index += 1
                obj.append_and_switch()
                return True
            case IsToken.RESET_CONTINUE:
                if obj.token:
                    obj.add_blacklist(type(obj.token))
                obj.reset()
                return False
            case IsToken.TRUE_CONTINUE:
                obj.index += 1
                return True
            case IsToken.FALSE_SKIP:
                obj.index += 1
                obj.append_and_switch()
                return False

    def __verify_char(
        self,
        obj: SolveData,
        char: str,
        tokens: Sequence[type[Token]],
        error_message: str,
    ):
        """
        Attempt to find what token
        this character may correlate with.
        """
        for i in tokens:
            if i in obj.blacklist:
                continue
            obj.set_token(i(self.stack, self.env))
            returned: IsToken = obj.token.add_char_to_token(  # type:ignore
                char
            )
            breakable = self.__resolve_token_return(obj, returned, char)
            if breakable:
                break
        else:
            raise ExpectedTokenError(self.stack, error_message)

    def __convert_string(self, obj: SolveData):
        """
        Convert the given string into
        a list of tokens; values, and
        operators.

        For example:
        5 * 5

        Will become:
        [<Number>, <Operator>, <Number>]
        """
        to_parse = self.value
        while obj.index < len(to_parse):
            char = to_parse[obj.index]

            if obj.token is None:
                if char.isspace():
                    obj.index += 1
                    obj.start_index += 1
                    continue
                self.__verify_char(
                    obj,
                    char,
                    self.value_types if not obj.is_operation else self.operands,
                    f"A valid {'operand' if obj.is_operation else 'value'} was expected",
                )
                continue

            value = obj.token.add_char_to_token(char)
            self.__resolve_token_return(obj, value, char, false_is_switch_operand=True)

        if obj.token and not obj.token.closed:
            obj.token.not_closed()
        elif obj.token:
            obj.append_and_switch()

        if len(obj.parse_list) % 2 == 0:
            raise ExpectedTokenError(
                self.stack, "Values are expected after an operator"
            )

    def __build_parse_trees(self, obj: SolveData):
        """
        This converts a list of
        tokens into one single
        token that can be solved.

        For example:
        [<Number>, <Operator>, <Number>]

        Will become:
        [<Operator left=Number right=Number>]

        This will allow us to tell the
        operator (the root of the tree)
        to solve the equation.

        Here's a more complicated example:
        [<Number>, <Multi>, <Number>, <Add>, <Number>]
        Will become:
        [<Multi left=<Number> right=<Add left=Number right=Number>>]
        """
        # for i in all operands in the language
        for the_type in self.operands:
            # for i in the precedence of that type of operand
            for i in the_type.precedence:
                index = 0
                while index < len(obj.parse_list):
                    token: Token = obj.parse_list[index]
                    if (
                        not isinstance(token, Operator)
                        or token.tree_set
                        or token.value not in i
                    ):
                        index += 1
                        continue

                    right = obj.parse_list.pop(index + 1)
                    left = obj.parse_list.pop(index - 1)
                    token.set_tree(left, right)
        if len(obj.parse_list) != 1:
            raise ExpectedTokenError(
                self.stack, f"Parsing failed. Size of root was {len(obj.parse_list)}"
            )

    def solve(self) -> token_return_types:
        """
        Solve the expression given
        to this token.
        """
        obj = SolveData()

        self.__convert_string(obj)

        self.__build_parse_trees(obj)

        solution = obj.parse_list[0].solve()

        if isinstance(solution, float) and solution.is_integer():
            solution = int(solution)

        if not self.is_opposite:
            return solution

        try:
            return not solution
        except Exception:
            raise UnexpectedTokenError(
                self.stack, "'!' is not accepted for the value given in this line."
            )

    @staticmethod
    def tokenize(
        string: str, stack: Any | None = None, env: Environment | None = None
    ) -> token_return_types:
        """
        Will simplify the expression
        given to a single data type.

        This function also supports
        the use of variables, and
        the environment.

        # Examples
        >>> tokenize("5+5")
        10
        >>> tokenize("10*10+10")
        110
        """
        x = Tokenizer(stack, env, string)
        return x.solve()

    @staticmethod
    def tokenize_all(
        strings: list[str], stack: Any | None = None, env: Environment | None = None
    ) -> list[token_return_types]:
        """
        Just like `tokenize`, but
        instead tokenizes a list
        of strings.

        # Examples
        >>> tokenize_all(["2+2", "5+5"])
        [4, 10]
        """
        returnable = []
        for i in strings:
            returnable.append(Tokenizer.tokenize(i, stack, env))
        return returnable
