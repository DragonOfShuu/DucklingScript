from __future__ import annotations

from typing import Any, Iterable, TYPE_CHECKING, Literal
from pathlib import Path

from ducklingscript.compiler.environments.packaged_variables import PackagedVariables

from .wrapped_function import WrappedFunction

from .function_type import Function
from .base_environment import BaseEnvironment
from ..errors import UnacceptableVarNameError, VarIsNonExistentError
from ..pre_line import PreLine
from .env_extend_type import EnvExtendType


if TYPE_CHECKING:
    from ..stack import Stack
    from .environment import Environment


class VariableEnvironment(BaseEnvironment):
    """
    An environment that stores
    variables.

    System Vars: Variables that are
    prefixed with a dollar sign ($),
    and are globals only settable
    by the system. You can only
    access these variables, not set
    them.

    User Vars: Variables that are
    defined by the user, and can be
    set and accessed freely.

    Temp Vars: Variables that are
    defined by the system, but
    are specific to this environment.

    Functions: Functions that are
    defined by the user, and can be
    called and accessed freely.
    """

    acceptable_vars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"

    def __init__(
        self,
        stack: "Stack | None" = None,
        owning_env: "Environment | None" = None,
        previous_env: VariableEnvironment | None = None,
        starter_system_vars: dict[str, Any] | None = None,
        starter_user_vars: dict[str, Any] | None = None,
        starter_temp_vars: dict[str, Any] | None = None,
        starter_functions: dict[str, WrappedFunction | Function] | None = None,
    ):
        self.system_vars = starter_system_vars or {}
        self.user_vars = starter_user_vars or {}
        self.temp_vars = starter_temp_vars or {}
        self.functions = starter_functions or {}
        
        self.expressed_variables: list[str] = []

        self.stack = stack
        self.owning_env = owning_env
        self.previous_env = previous_env

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
        # Because system vars are global,
        # we check the previous environment
        # and create the variable there if it exists.
        if self.previous_env:
            return self.previous_env.new_system_var(name, value)

        name = self.conv_to_sys_var(name)

        self.verify_var_name(name)
        self.system_vars.update({name: value})

    def new_user_var(self, name: str, value: Any):
        """
        Create a new user defined
        variable.
        """
        self.verify_var_name(name, can_be_sys_var=False)

        # The reason we check previous environments
        # is because any time `VAR` is used, it
        # creates a new variable. On top of this,
        # doing it this way avoids a sort of `GLOBAL`
        # keyword, and since DucklingScript is a smaller
        # language, if people want to separate things out
        # they should just make a new file. This may be
        # changed in the future though.

        # See if we can edit a previous environment
        # if it exists first
        if self.previous_env and self.previous_env.edit_user_var(name, value):
            return True

        # If we can't, we create a new variable
        # in this environment.
        self.user_vars.update({name: value})

    def hard_new_var(self, name: str, value: Any):
        """
        Create a new variable
        that is directly on this environment,
        skipping checking previous environments.
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

        self.functions.update(
            {name: Function(name=name, arguments=arguments, code=code, file=file)}
        )

        # Why did I do this? Keeping this
        # here in case I wasn't actually
        # off my rocker. Wrapped functions
        # should only be created by
        # import/export systems.
        # ====================
        # if not self.owning_env:
        #     raise ValueError(
        #         "Included stack must contain an environment to own the function."
        #     )

        # self.functions.update({
        #     name: WrappedFunction(
        #         environment=self.owning_env,
        #         function=Function(name=name, arguments=arguments, code=code, file=file),
        #     )
        # })
    
    def express_var(self, name: str):
        if name in self.user_vars or name in self.functions:
            self.expressed_variables.append(name)
            return
        raise VarIsNonExistentError(f'"{name}" variable does not exist, and cannot be expressed.')

    def edit_user_var(self, name: str, value: Any) -> bool:
        """
        Edit a user defined
        variable.

        Return true if successful. Runs
        recursively through previous
        environments if the variable is not found here.
        """
        if name in self.user_vars:
            self.user_vars[name] = value
            return True

        if self.previous_env:
            return self.previous_env.edit_user_var(name, value)

        return False

    def edit_system_var(self, name: str, value: Any):
        """
        Edit a system defined
        variable.
        """
        if self.previous_env:
            return self.previous_env.edit_system_var(name, value)

        name = self.conv_to_sys_var(name)

        if name not in self.system_vars:
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

        if name not in self.temp_vars:
            raise VarIsNonExistentError(
                self.stack,
                "Attempted edit on non-existent temp var (This error SHOULD NOT occur under any normal circumstances)",
            )

        self.temp_vars[name] = value

    def delete_user_var(self, name: str) -> bool:
        """
        Delete a user
        var by name.
        """
        if self.user_vars.get(name, None) is not None:
            self.user_vars.pop(name)
            return True

        if self.previous_env and self.previous_env.delete_user_var(name):
            return True

        return False

    def delete_system_var(self, name: str) -> bool:
        """
        Delete a system
        var by name.
        """
        if self.system_vars.get(name, None) is not None:
            self.system_vars.pop(name)
            return True

        if self.previous_env and self.previous_env.delete_system_var(name):
            return True

        return False

    def delete_temp_var(self, name: str) -> bool:
        """
        Delete a temp
        var by name.
        """
        if self.temp_vars.get(name, None) is not None:
            self.temp_vars.pop(name)
            return True
        return False

    def get_system_var(self, name: str) -> Any:
        """
        Get a system variable
        by name.
        """
        if self.previous_env:
            return self.previous_env.get_system_var(name)

        if name in self.system_vars:
            return self.system_vars[name]
        
        raise VarIsNonExistentError(
            self.stack,
            f"Attempted to get non-existent system var '{name}'."
        )

    def get_user_var(self, name: str) -> Any:
        """
        Get a user defined
        variable by name.
        """
        if name in self.user_vars:
            return self.user_vars[name]
        if self.previous_env and (value := self.previous_env.get_user_var(name)) is not None:
            return value
        raise VarIsNonExistentError(
            self.stack,
            f"Attempted to get non-existent user var '{name}'.")

    def get_function(self, name: str) -> WrappedFunction | Function:
        """
        Get a function by name.
        """
        if name in self.functions:
            return self.functions[name]
        
        if self.previous_env and (value := self.previous_env.get_function(name)) is not None:
            return value
        
        raise VarIsNonExistentError(
            self.stack,
            f"Attempted to get non-existent function '{name}'."
        )
    
    def get_temp_var(self, name: str) -> Any:
        if name in self.temp_vars:
            return self.temp_vars[name]
        
        raise VarIsNonExistentError(
            self.stack,
            f"Attempted to get non-existent temp var '{name}'."
        )

    @property
    def all_vars(self):
        """
        All stored variables,
        not including functions,
        across all environments.
        """
        all_vars = {
            **self.get_system_vars(),
            **self.get_temp_vars(),
            **self.get_user_vars(),
        }
        return all_vars

    def get_system_vars(self) -> dict[str, Any]:
        """
        Get all system variables.
        """
        if self.previous_env:
            return self.previous_env.get_system_vars()
        return self.system_vars

    def get_user_vars(self) -> dict[str, Any]:
        """
        Get all user defined variables.

        DO NOT SET. The returned value is disconnected from the environment
        and any changes made to it will not affect the environment.
        """
        if self.previous_env:
            return {**self.previous_env.get_user_vars(), **self.user_vars}
        return self.user_vars.copy()

    def get_temp_vars(self) -> dict[str, Any]:
        """
        Get all temporary variables.

        Temp variables only include the variables defined in this environment.
        """
        return self.temp_vars

    def export_variables(
        self, variable_names: list[str] | Literal[True] | None = None, wrap: bool = True
    ) -> PackagedVariables:
        """
        Provides variables from this environment,
        optionally wrapped with the environment context
        (true by default). 

        For `variable_names`, if `list[str]` is provided,
        those variables will be exported. If `True`, 
        expressed variables will be exported. If `None`,
        all variables will be exported.
        """
        if variable_names is True:
            names_to_process = self.expressed_variables
        elif variable_names:
            names_to_process = variable_names
            user_vars = {
                name: self.user_vars[name]
                for name in names_to_process
                if name in self.user_vars
            }
            functions = {
                name: self.functions[name]
                for name in names_to_process
                if name in self.functions
            }
        else:
            user_vars = self.user_vars
            functions = self.functions

        if not wrap:
            return PackagedVariables(user_vars=user_vars, functions=functions)

        owning_env = self.owning_env
        if not owning_env:
            raise RuntimeError(
                "Owning environment must be initialized to export wrapped variables."
            )

        return PackagedVariables.create_wrapped(owning_env, user_vars, functions)

    def import_variables(self, variables: PackagedVariables):
        user_vars = variables.user_vars
        function_vars = variables.functions
        for name, value in user_vars.items():
            self.new_user_var(name, value)
        for name, value in function_vars.items():
            self.functions.update({name: value})

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

    def extend_env(
        self,
        stack: "Stack|None",
        owning_env: "Environment|None",
        extend_type: EnvExtendType,
    ) -> VariableEnvironment:
        """
        Extend the environment to a parallel
        environment if parallel is True.
        """
        match extend_type:
            case EnvExtendType.PARALLEL:
                return VariableEnvironment(
                    stack=stack,
                    owning_env=owning_env,
                    previous_env=self,
                    starter_system_vars=self.system_vars,
                    starter_user_vars=self.user_vars,
                    starter_functions=self.functions,
                )
            case EnvExtendType.NORMAL:
                return VariableEnvironment(
                    stack=stack,
                    owning_env=owning_env,
                    previous_env=self,
                )
            case EnvExtendType.HARD:
                return VariableEnvironment(
                    stack=stack,
                    owning_env=owning_env,
                    previous_env=None,
                    starter_system_vars=self.system_vars.copy(),
                )
