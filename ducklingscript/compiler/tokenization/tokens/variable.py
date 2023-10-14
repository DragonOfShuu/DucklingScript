from typing import Any
from ducklingscript.compiler.environment import Environment
from .token import Token


class Variable(Token):
    # def __init__(self, stack: Any, environ: Environment):
    #     self.environ = environ
    #     super().__init__(stack, environ)

    def init_token_vars(self):
        self.vars = self.environ.all_vars
        self.keywords = list(self.vars.keys())
        self.init_keyword_vars()

    def set_value(self, value: str):
        if value not in self.vars:
            raise ValueError(
                f"String {value} was recognized as a variable, but was not one."
            )
        self.value = self.vars.get(value)
