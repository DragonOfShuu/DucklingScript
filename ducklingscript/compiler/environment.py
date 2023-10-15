from typing import Any, Iterable
from dataclasses import dataclass
from .errors import VarIsNonExistent, UnacceptableVarName


@dataclass
class Function:
    name: str
    arguments: list[str]
    code: list[str]


class Null:
    pass


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
        self.stack = stack

        self.verify_names(system_vars.keys())
        self.verify_names(user_vars.keys())
        self.verify_names([i.name for i in functions])

        self.system_vars = system_vars
        self.user_vars = user_vars
        self.functions = functions

    def verify_var_name(self, name: str):
        if not self.is_var:
            raise UnacceptableVarName(
                self.stack,
                f"'{name}' is not a valid variable name. Acceptable names include all letters, numbers after any letter (only), and underscores.",
            )

    def verify_names(self, names: Iterable[str]):
        for i in names:
            self.verify_var_name(i)

    @classmethod
    def is_var(cls, name: str) -> bool:
        for count, i in enumerate(name):
            if count == 0 and i.isdigit():
                return False
            if i not in cls.acceptable_vars:
                return False
        return True

    def new_system_var(self, name: str, value: Any):
        name = self.conv_to_sys_var(name)

        self.verify_var_name(name)
        self.system_vars.update({name: value})

    def new_var(self, name: str, value: Any):
        self.verify_var_name(name)
        self.user_vars.update({name: value})

    def new_function(self, name: str, arguments: list[str], code: list[str]):
        self.verify_var_name(name)
        self.functions.append(Function(name, arguments, code))

    def edit_user_var(self, name: str, value: Any):
        var_value = self.user_vars.get(name, Null())
        if isinstance(var_value, Null):
            raise VarIsNonExistent(
                self.stack, "Attempted edit on non-existent user var"
            )

        self.user_vars[name] = value

    def edit_system_var(self, name: str, value: Any):
        name = self.conv_to_sys_var(name)
        var_value = self.user_vars.get(name, Null())
        if isinstance(var_value, Null):
            raise VarIsNonExistent(
                self.stack, "Attempted edit on non-existent user var"
            )

        self.user_vars[name] = value

    @property
    def all_vars(self):
        all_vars = {}
        all_vars.update(self.system_vars)
        all_vars.update(self.user_vars)
        return all_vars

    @staticmethod
    def conv_to_sys_var(var: str):
        return var if var.startswith("$") else f"${var}"
