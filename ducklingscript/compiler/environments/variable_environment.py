from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable
from pathlib import Path

from .base_environment import BaseEnvironment
from ..errors import UnacceptableVarNameError, VarIsNonExistentError
from ..pre_line import PreLine


@dataclass
class Function:
    name: str
    arguments: list[str]
    code: list[PreLine | list]
    file: str | Path | None


class Null:
    pass


class VariableEnvironment(BaseEnvironment):
    """
    An environment that stores
    variables.
    """

    acceptable_vars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"

    def __init__(
        self,
        stack: Any | None = None,
        system_vars: dict[str, Any] | None = None,
        user_vars: dict[str, Any] | None = None,
        temp_vars: dict[str, Any] | None = None,
        functions: dict[str, Function] | None = None,
    ):
        self.system_vars = {} if system_vars is None else system_vars
        self.user_vars = {} if user_vars is None else user_vars
        self.temp_vars = {} if temp_vars is None else temp_vars
        self.functions = {} if functions is None else functions

        self.stack = stack

        self.verify_names(self.conv_to_sys_vars(self.system_vars.keys()))
        self.verify_names(self.user_vars.keys(), can_be_sys_var=False)
        self.verify_names(self.conv_to_sys_vars(self.temp_vars.keys()))
        self.verify_names(self.functions.keys(), can_be_sys_var=False)

    def verify_var_name(self, name: str, can_be_sys_var: bool = True):
        """
        Check if the name is
        a valid variable name.

        !!! This function calls an error if it is not a variable !!!
        """
        if not self.is_var(name, can_be_sys_var):
            raise UnacceptableVarNameError(
                self.stack,
                f"'{name}' is not a valid variable name. Acceptable names include all letters, numbers after any letter (only), and underscores.",
            )

    def verify_names(self, names: Iterable[str], can_be_sys_var: bool = True):
        """
        Check if all names
        given are valid
        variable names.

        !!! This function calls an error if it is not a variable !!!
        """
        for i in names:
            self.verify_var_name(i, can_be_sys_var)

    @classmethod
    def is_var(cls, name: str, can_be_sys_var: bool = True) -> bool:
        """
        Check if the name is
        a valid variable name.

        Returns False if the
        variable is not valid.
        """
        for count, i in enumerate(name):
            if count == 0 and i == "$":
                if can_be_sys_var:
                    continue
                else:
                    return False

            if count == 0 and i.isdigit():
                return False

            if i not in cls.acceptable_vars:
                return False
        return True

    def new_system_var(self, name: str, value: Any):
        """
        Create a new system variable.

        Please note that the user can get
        these variables using the '$' operator,
        but should not be able to set
        them.
        """
        name = self.conv_to_sys_var(name)

        self.verify_var_name(name)
        self.system_vars.update({name: value})

    def new_var(self, name: str, value: Any):
        """
        Create a new user defined
        variable.
        """
        self.verify_var_name(name, can_be_sys_var=False)
        self.user_vars.update({name: value})

    def new_temp_var(self, name: str, value: Any):
        """
        Create a new temporary
        variable.
        """
        name = self.conv_to_sys_var(name)

        self.verify_var_name(name)
        self.temp_vars.update({name: value})

    def new_function(
        self,
        name: str,
        arguments: list[str],
        code: list[PreLine | list],
        file: str | Path | None,
    ):
        """
        Create a new funciton.
        """
        self.verify_var_name(name, can_be_sys_var=False)
        self.verify_names(arguments, can_be_sys_var=False)
        self.functions.update({name: Function(name, arguments, code, file)})

    def edit_user_var(self, name: str, value: Any):
        """
        Edit a user defined
        variable.
        """
        var_value = self.user_vars.get(name, Null())
        if isinstance(var_value, Null):
            raise VarIsNonExistentError(
                self.stack, "Attempted edit on non-existent user var"
            )

        self.user_vars[name] = value

    def edit_system_var(self, name: str, value: Any):
        """
        Edit a system defined
        variable.
        """
        name = self.conv_to_sys_var(name)
        var_value = self.system_vars.get(name, Null())
        if isinstance(var_value, Null):
            raise VarIsNonExistentError(
                self.stack,
                "Attempted edit on non-existent system var (This error SHOULD NOT occur under any normal circumstances)",
            )

        self.system_vars[name] = value

    def edit_temp_var(self, name: str, value: Any):
        """
        Edit a temp defined
        variable.
        """
        name = self.conv_to_sys_var(name)

        var_value = self.temp_vars.get(name, Null())
        if isinstance(var_value, Null):
            raise VarIsNonExistentError(
                self.stack,
                "Attempted edit on non-existent temp var (This error SHOULD NOT occur under any normal circumstances)",
            )

        self.temp_vars[name] = value

    def delete_user_var(self, name: str):
        """
        Delete a user
        var by name.
        """
        if self.user_vars.get(name, None) is not None:
            self.user_vars.pop(name)

    def delete_system_var(self, name: str):
        """
        Delete a system
        var by name.
        """
        if self.system_vars.get(name, None) is not None:
            self.system_vars.pop(name)

    def delete_temp_var(self, name: str):
        """
        Delete a temp
        var by name.
        """
        if self.temp_vars.get(name, None) is not None:
            self.temp_vars.pop(name)

    @property
    def all_vars(self):
        """
        All stored variables,
        not including functions.
        """
        all_vars = {}
        all_vars.update(self.system_vars)
        all_vars.update(self.temp_vars)
        all_vars.update(self.user_vars)
        return all_vars

    @staticmethod
    def conv_to_sys_var(var: str):
        """
        Add dollar sign
        to the front of a
        variable.
        """
        return var if var.startswith("$") else f"${var}"

    @staticmethod
    def conv_to_sys_vars(var: Iterable[str]):
        """
        Add dollar sign
        to the front of
        multiple variables.
        """
        return [(f"${v}" if not v.startswith("$") else v) for v in var]

    def update_from_env(self, env: VariableEnvironment):
        """
        Overwrite self variables
        with the environment given.
        Does not add new variables.
        """
        sys_vars = env.system_vars
        user_vars = env.user_vars

        new_sys_vars = {
            i: sys_vars[i] for i in self.system_vars.keys() if i in sys_vars
        }
        new_user_vars = {
            i: user_vars[i] for i in self.user_vars.keys() if i in user_vars
        }

        self.system_vars = new_sys_vars
        self.user_vars = new_user_vars

    def append_env(self, env: VariableEnvironment):
        """
        Overwrite self variables
        with the environment given.
        This *will* add new variables.
        """
        self.user_vars.update(env.user_vars)
        self.system_vars.update(env.system_vars)
        self.functions.update(env.functions)
