from .token import Token
from .operator import Operator

from .number import Number
from .string import String
from .boolean import Boolean
from .variable import Variable

from .math_operator import MathOperator
from .conditional_operator import ConditionalOperator

value_types: list[type[Token]] = [String, Number, Boolean, Variable]
operands: list[type[Operator]] = [MathOperator, ConditionalOperator]

isToken = Token.isToken
