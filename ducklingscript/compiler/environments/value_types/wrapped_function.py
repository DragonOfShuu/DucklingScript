from typing import TYPE_CHECKING, Any

from ...errors import InvalidArgumentsError
from ...tokenization.token_value_types import Function
from .wrapped_variable import WrappedVariable

if TYPE_CHECKING:
    from ..environment import Environment
    from ...stack import Stack


class WrappedFunction(WrappedVariable):
    """
    A class to wrap a function in the environment.
    This allows the function to be called with arguments.
    """

    def __init__(self, environment: "Environment", function: Function):
        super().__init__(environment, function)

    def _function_type_guard(self, value: Any) -> Function:
        """
        Ensure that the wrapped value is a Function.
        """
        if not isinstance(value, Function):
            raise TypeError(f"WrappedFunction: {value} is not a Function.")
        return value

    @property
    def value(self) -> Function:
        self._function_type_guard(self._value)
        return self._value

    @value.setter
    def value(self, new_value: Function):
        self._function_type_guard(new_value)
        self._value = new_value
        return new_value

    def call_value(self, current_stack: "Stack", *args: Any):
        """
        Call the wrapped data as a function.
        """
        self._function_type_guard(self._value)

        function = self._value

        stack_pile = current_stack.stack_pile

        if len(function.arguments) != len(args):
            raise InvalidArgumentsError(
                current_stack,
                f"{len(args)} arguments were given when {len(function.arguments)} was expected.",
            )

        with stack_pile.add_stack_above(
            function.code, function.file, injectable_env=self.environment
        ) as st:
            for count, name in enumerate(function.arguments):
                st.env.var.new_user_var(name, args[count])

            compiled = st.run()

        return compiled
