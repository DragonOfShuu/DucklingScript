from typing import Any
from dataclasses import dataclass
from .errors import VarIsNonExistent


@dataclass
class Function:
    name: str
    arguments: list[str]
    code: list[str]


# If this language was object oriented,
# everything would be objects, and they
# would have attributes that flow with
# the language, like functions would
# just have something similar to Python's
# __call__ dunder.

# However this language doesn't know
# what an object is, so instead
# I'll just keep things functional.


class Environment:
    def __init__(
        self,
        system_vars: dict[str, Any] = {},
        user_vars: dict[str, Any] = {},
        functions: list[Function] = [],
    ):
        self.system_vars = system_vars
        self.user_vars = user_vars
        self.functions = functions

    def new_system_var(self, name: str, value: Any):
        self.system_vars.update({name: value})

    def new_var(self, name: str, value: Any):
        self.user_vars.update({name: value})

    def new_function(self, name: str, arguments: list[str], code: list[str]):
        self.functions.append(Function(name, arguments, code))

    def parse_vars(
        self,
        text: str,
        system_vars: bool = True,
        user_vars: bool = True,
        in_string: bool = True,
    ):
        if in_string:
            self.parse_string_var(text, system_vars, user_vars)
        else:
            self.parse_expression_var(text, system_vars, user_vars)

    def parse_string_var(self, text: str, system_vars: bool, user_vars: bool):
        # "Hello {name}!"
        pass

    def parse_expression_var(self, text: str, system_vars: bool, user_vars: bool):
        # name + 1
        pass
    
    # acceptable_vars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"