from __future__ import annotations

from .value_types.function_type import Function
from ..tokenization.token_value_types import UnwrappedTokenValueTypes
from .value_types.wrapped_variable import WrappedVariable

from .value_types.wrapped_function import WrappedFunction

from dataclasses import dataclass, field
from typing import Any, Mapping, TYPE_CHECKING, Type, cast

if TYPE_CHECKING:
    from .environment import Environment


class VariablePackager:
    @classmethod
    def wrap_recursively(cls, value: Any, type: Type[WrappedVariable], env: "Environment") -> WrappedVariable:
        if isinstance(value, dict):
            return type(env, {k: cls.wrap_recursively(v, type, env) for k, v in value.items()})
        else:
            return type(env, value)

    @classmethod
    def unwrap_variable(cls, var_list: Mapping[str, WrappedVariable]) -> Mapping[str, Any]:
        return {k: (v.value if not isinstance(v.value, dict) else cls.unwrap_variable(v.value)) for k, v in var_list.items()}

    @classmethod
    def unwrap_variables(cls, var_lists: list[Mapping[str, WrappedVariable]]) -> list[Mapping[str, Mapping[str, Any]]]:
        return [cls.unwrap_variable(v) for v in var_lists]

    @classmethod
    def wrap_variable(cls, var_list: Mapping[str, Any], type: Type[WrappedVariable], env: "Environment") -> Mapping[str, WrappedVariable]:
        return {k: cls.wrap_recursively(v, type, env) for k, v in var_list.items()}

    @classmethod
    def wrap_variables(cls, var_lists: list[Mapping[str, Any]], type: Type[WrappedVariable], env: "Environment") -> list[Mapping[str, WrappedVariable]]:
        return [cls.wrap_variable(v, type, env) for v in var_lists]
    
    @classmethod
    def rewrap_variable(cls, var_list: Mapping[str, Any], type: Type[WrappedVariable], env: "Environment") -> Mapping[str, WrappedVariable]:
        return {k: VariablePackager.wrap_recursively(v, type, env) for k, v in var_list.items()}
    
    @classmethod
    def rewrap_variables(cls, var_lists: list[Mapping[str, Any]], type: Type[WrappedVariable], env: "Environment") -> list[Mapping[str, WrappedVariable]]:
        return [cls.rewrap_variable(v, type, env) for v in var_lists]


@dataclass
class PackagedVariables:
    """
    PackagedVariables is a container for various types of variables
    used in the DucklingScript environment.

    This is used for when an environment needs to pass its variables to
    another environment.

    Since they are wrapped, they can reference the original environment
    while still being in a different environment.
    """

    user_vars: Mapping[str, WrappedVariable] = field(default_factory=dict)
    functions: Mapping[str, WrappedFunction] = field(default_factory=dict)
    temp_vars: Mapping[str, WrappedVariable] = field(default_factory=dict)
    system_vars: Mapping[str, WrappedVariable] = field(default_factory=dict)

    def unwrap_vars(self) -> "UnwrappedPackagedVariables":
        """
        Unwraps the variables in this PackagedVariables instance using VariablePackager.
        """
        return UnwrappedPackagedVariables(
            user_vars=VariablePackager.unwrap_variable(self.user_vars),
            functions=VariablePackager.unwrap_variable(self.functions),
            temp_vars=VariablePackager.unwrap_variable(self.temp_vars),
            system_vars=VariablePackager.unwrap_variable(self.system_vars),
        )

    def rewrap_vars(self, env: "Environment") -> "PackagedVariables":
        """
        Rewraps the variables in this PackagedVariables instance using the provided environment.
        This is useful when transferring variables to a new environment where you don't want
        to reference the original environment.
        """
        wrapped_user_vars = VariablePackager.rewrap_variable(self.user_vars, WrappedVariable, env)
        wrapped_functions = VariablePackager.rewrap_variable(self.functions, WrappedFunction, env)
        wrapped_temp_vars = VariablePackager.rewrap_variable(self.temp_vars, WrappedVariable, env)
        wrapped_system_vars = VariablePackager.rewrap_variable(self.system_vars, WrappedVariable, env)

        return PackagedVariables(
            user_vars=wrapped_user_vars,
            functions=cast(Mapping[str, WrappedFunction], wrapped_functions),
            temp_vars=wrapped_temp_vars,
            system_vars=wrapped_system_vars,
        )


@dataclass
class UnwrappedPackagedVariables:
    """
    UnwrappedPackagedVariables is a container for various types of variables
    used in the DucklingScript environment.

    This is often used when passing variables to a new environment (often
    the root environment).

    Since they are unwrapped, they are not tethered
    to a specific environment and can be used independently.
    """
    user_vars: Mapping[str, UnwrappedTokenValueTypes] = field(default_factory=dict)
    functions: Mapping[str, Function] = field(default_factory=dict)
    temp_vars: Mapping[str, UnwrappedTokenValueTypes] = field(default_factory=dict)
    system_vars: Mapping[str, UnwrappedTokenValueTypes] = field(default_factory=dict)

    def wrap_vars(self, env: "Environment") -> "PackagedVariables":
        """
        Wraps the variables in this UnwrappedPackagedVariables instance using the provided environment.
        """
        wrapped_user_vars = VariablePackager.wrap_variable(self.user_vars, WrappedVariable, env)
        wrapped_functions = VariablePackager.wrap_variable(self.functions, WrappedFunction, env)
        wrapped_temp_vars = VariablePackager.wrap_variable(self.temp_vars, WrappedVariable, env)
        wrapped_system_vars = VariablePackager.wrap_variable(self.system_vars, WrappedVariable, env)

        return PackagedVariables(
            user_vars=wrapped_user_vars,
            functions=cast(Mapping[str, WrappedFunction], wrapped_functions),
            temp_vars=wrapped_temp_vars,
            system_vars=wrapped_system_vars,
        )
