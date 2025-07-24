from __future__ import annotations

from .function_type import Function
from ..tokenization.token_value_types import TokenValueTypes
from .wrapped_variable import WrappedVariable

from .wrapped_function import WrappedFunction

from dataclasses import dataclass, field
from typing import Mapping, TYPE_CHECKING

if TYPE_CHECKING:
    from .environment import Environment


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
        unwrapped_user_vars = {k: v.value for k, v in self.user_vars.items()}
        unwrapped_functions = {k: v.value for k, v in self.functions.items()}
        unwrapped_temp_vars = {k: v.value for k, v in self.temp_vars.items()}
        unwrapped_system_vars = {k: v.value for k, v in self.system_vars.items()}

        return UnwrappedPackagedVariables(
            user_vars=unwrapped_user_vars,
            functions=unwrapped_functions,
            temp_vars=unwrapped_temp_vars,
            system_vars=unwrapped_system_vars,
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
    user_vars: Mapping[str, TokenValueTypes] = field(default_factory=dict)
    functions: Mapping[str, Function] = field(default_factory=dict)
    temp_vars: Mapping[str, TokenValueTypes] = field(default_factory=dict)
    system_vars: Mapping[str, TokenValueTypes] = field(default_factory=dict)

    def wrap_vars(self, env: "Environment"):
        """
        Wraps the variables in this PackagedVariables instance using the provided environment.
        """
        wrapped_user_vars = {
            k: WrappedVariable(env, v) for k, v in self.user_vars.items()
        }
        wrapped_functions = {
            k: WrappedFunction(env, v) for k, v in self.functions.items()
        }
        wrapped_temp_vars = {
            k: WrappedVariable(env, v) for k, v in self.temp_vars.items()
        }
        wrapped_system_vars = {
            k: WrappedVariable(env, v) for k, v in self.system_vars.items()
        }

        return PackagedVariables(
            user_vars=wrapped_user_vars,
            functions=wrapped_functions,
            temp_vars=wrapped_temp_vars,
            system_vars=wrapped_system_vars,
        )
