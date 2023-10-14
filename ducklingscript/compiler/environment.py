from typing import Any, Iterable
from dataclasses import dataclass
from .errors import VarIsNonExistent, UnacceptableVarName


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
    acceptable_vars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"

    def __init__(
        self,
        system_vars: dict[str, Any] = {},
        user_vars: dict[str, Any] = {},
        functions: list[Function] = [],
        stack: Any | None = None,
    ):
        self.system_vars = system_vars
        self.user_vars = user_vars
        self.functions = functions
        self.stack = stack

    def __verify_var_name(self, name: str):
        for i in name:
            if i not in self.acceptable_vars:
                raise UnacceptableVarName(
                    self.stack,
                    f"'{name}' is not a valid variable name. ({i} is not acceptable)",
                )

    def __verify_names(self, names: Iterable[str]):
        for i in names:
            self.__verify_var_name(i)

    def new_system_var(self, name: str, value: Any):
        self.__verify_var_name(name)
        self.system_vars.update({name: value})

    def new_var(self, name: str, value: Any):
        self.__verify_var_name(name)
        self.user_vars.update({name: value})

    def new_function(self, name: str, arguments: list[str], code: list[str]):
        self.__verify_var_name(name)
        self.functions.append(Function(name, arguments, code))

    @property
    def all_vars(self):
        all_vars = {}
        all_vars.update(self.system_vars)
        all_vars.update(self.user_vars)
        return all_vars

    # def parse_vars(
    #     self,
    #     text: str,
    #     system_vars: bool = True,
    #     user_vars: bool = True,
    #     in_string: bool = True,
    # ):
    #     if in_string:
    #         self.parse_string_var(text, system_vars, user_vars)
    #     else:
    #         self.parse_expression_var(text, system_vars, user_vars)

    # def parse_string_var(self, text: str, system_vars: bool, user_vars: bool):
    #     # "Hello {name}!"
    #     pass

    # def parse_expression_var(self, text: str, system_vars: bool, user_vars: bool):
    #     # name + 1
    #     pass
