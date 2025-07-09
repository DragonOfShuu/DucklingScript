from .function_type import Function
from .wrapped_function import WrappedFunction

from dataclasses import dataclass, field
from typing import Any, Mapping, TYPE_CHECKING

if TYPE_CHECKING:
    from .environment import Environment


@dataclass
class PackagedVariables:
    user_vars: Mapping[str, Any] = field(default_factory=dict)
    functions: Mapping[str, WrappedFunction | Function] = field(default_factory=dict)

    @classmethod
    def create_wrapped(
        cls,
        environment: "Environment",
        user_vars: Mapping[str, Any],
        functions: Mapping[str, WrappedFunction | Function],
    ):
        wrapped_functions = {
            name: (
                WrappedFunction(environment, func)
                if isinstance(func, Function)
                else func
            )
            for name, func in functions.items()
        }

        return cls(user_vars=user_vars, functions=wrapped_functions)
