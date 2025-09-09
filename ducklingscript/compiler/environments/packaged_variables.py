from __future__ import annotations

from .value_types.function_type import Function
from ..tokenization.token_value_types import UnwrappedTokenValueTypes
from .value_types.wrapped_variable import WrappedVariable

from .value_types.wrapped_function import WrappedFunction

from dataclasses import dataclass, field
from typing import Any, Mapping, TYPE_CHECKING, Type, cast

if TYPE_CHECKING:
    from .environment import Environment


def wrap_recursively(value: Any, type: Type[WrappedVariable], env: Environment) -> WrappedVariable:
    if isinstance(value, dict):
        return type(env, {k: wrap_recursively(v, type, env) for k, v in value.items()})
    else:
        return type(env, value)

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
        Unwraps the variables in this PackagedVariables instance.
        """

        def unwrap_variable(var_list: Mapping[str, WrappedVariable]) -> Mapping[str, Any]:
            return {k: (v.value if not isinstance(v.value, dict) else unwrap_variable(v.value)) for k, v in var_list.items()}

        unwrapped_user_vars = unwrap_variable(self.user_vars)
        unwrapped_functions = unwrap_variable(self.functions)
        unwrapped_temp_vars = unwrap_variable(self.temp_vars)
        unwrapped_system_vars = unwrap_variable(self.system_vars)

        return UnwrappedPackagedVariables(
            user_vars=unwrapped_user_vars,
            functions=unwrapped_functions,
            temp_vars=unwrapped_temp_vars,
            system_vars=unwrapped_system_vars,
        )

    def rewrap_vars(self, env: "Environment") -> PackagedVariables:
        """
        Rewraps the variables in this PackagedVariables instance using the provided environment.
        This is useful when transferring variables to a new environment where you don't want
        to reference the original environment.
        """

        def rewrap_variable(var_list: Mapping[str, Any], type: Type[WrappedVariable]) -> Mapping[str, WrappedVariable]:
            return {k: wrap_recursively(v.value, type, env) for k, v in var_list.items()}

        wrapped_user_vars = rewrap_variable(self.user_vars, WrappedVariable)
        wrapped_functions = rewrap_variable(self.functions, WrappedFunction)
        wrapped_temp_vars = rewrap_variable(self.temp_vars, WrappedVariable)
        wrapped_system_vars = rewrap_variable(self.system_vars, WrappedVariable)

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

    def wrap_vars(self, env: "Environment"):
        """
        Wraps the variables in this PackagedVariables instance using the provided environment.
        """

        def wrap_variable(var_list: Mapping[str, Any], type: Type[WrappedVariable]) -> Mapping[str, WrappedVariable]:
            return {k: wrap_recursively(v, type, env) for k, v in var_list.items()}

        wrapped_user_vars = wrap_variable(self.user_vars, WrappedVariable)
        wrapped_functions = wrap_variable(self.functions, WrappedFunction)
        wrapped_temp_vars = wrap_variable(self.temp_vars, WrappedVariable)
        wrapped_system_vars = wrap_variable(self.system_vars, WrappedVariable)

        return PackagedVariables(
            user_vars=wrapped_user_vars,
            functions=cast(Mapping[str, WrappedFunction], wrapped_functions),
            temp_vars=wrapped_temp_vars,
            system_vars=wrapped_system_vars,
        )
