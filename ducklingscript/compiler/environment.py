from typing import Any, Iterable
from dataclasses import dataclass
from .errors import VarIsNonExistent, UnacceptableVarName
from .pre_line import PreLine


@dataclass
class Function:
    name: str
    arguments: list[str]
    code: list[PreLine]


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
        '''
        Check if the name is
        a valid variable name.

        !!! This function calls an error if it is not a variable !!!
        '''
        if not self.is_var(name):
            raise UnacceptableVarName(
                self.stack,
                f"'{name}' is not a valid variable name. Acceptable names include all letters, numbers after any letter (only), and underscores.",
            )

    def verify_names(self, names: Iterable[str]):
        '''
        Check if all names 
        given are valid
        variable names.
        '''
        for i in names:
            self.verify_var_name(i)

    @classmethod
    def is_var(cls, name: str) -> bool:
        '''
        Check if the name is
        a valid variable name.

        Returns False if the
        variable is not valid.
        '''
        for count, i in enumerate(name):
            if count == 0 and i.isdigit():
                return False
            elif count == 0 and i=='$':
                return True
            if i not in cls.acceptable_vars:
                return False
        return True

    def new_system_var(self, name: str, value: Any):
        '''
        Create a new system variable.

        Please note that the user can get
        these variables using the '$' operator,
        but should not be able to set
        them.
        '''
        name = self.conv_to_sys_var(name)

        self.verify_var_name(name)
        self.system_vars.update({name: value})

    def new_var(self, name: str, value: Any):
        '''
        Create a new user defined
        variable.
        '''
        self.verify_var_name(name)
        self.user_vars.update({name: value})

    def new_function(self, name: str, arguments: list[str], code: list[PreLine]):
        '''
        Create a new funciton.
        '''
        self.verify_var_name(name)
        self.functions.append(Function(name, arguments, code))

    def edit_user_var(self, name: str, value: Any):
        '''
        Edit a user defined
        variable.
        '''
        var_value = self.user_vars.get(name, Null())
        if isinstance(var_value, Null):
            raise VarIsNonExistent(
                self.stack, "Attempted edit on non-existent user var"
            )

        self.user_vars[name] = value

    def edit_system_var(self, name: str, value: Any):
        '''
        Edit a system defined
        variable.
        '''
        name = self.conv_to_sys_var(name)
        var_value = self.system_vars.get(name, Null())
        if isinstance(var_value, Null):
            raise VarIsNonExistent(
                self.stack, "Attempted edit on non-existent user var"
            )

        self.system_vars[name] = value

    @property
    def all_vars(self):
        '''
        All stored variables,
        not including functions.
        '''
        all_vars = {}
        all_vars.update(self.system_vars)
        all_vars.update(self.user_vars)
        return all_vars

    @staticmethod
    def conv_to_sys_var(var: str):
        '''
        Add dollar sign
        to the front of a 
        variable.
        '''
        return var if var.startswith("$") else f"${var}"
