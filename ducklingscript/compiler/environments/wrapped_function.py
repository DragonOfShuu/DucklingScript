from typing import TYPE_CHECKING, Any

from ..errors import InvalidArgumentsError
from .function_object import Function
from .wrapped_data import WrappedData, WrappedDataType

if TYPE_CHECKING:
    from .environment import Environment
    from ..stack import Stack


class WrappedFunction(WrappedData):
    """
    A class to wrap a function in the environment.
    This allows the function to be called with arguments.
    """

    def __init__(self, environment: "Environment", function: Function):
        super().__init__(environment, WrappedDataType.FUNCTION, function)

    @property
    def value(self) -> Function:
        value = self._value
        if not isinstance(value, Function):
            raise TypeError(f"WrappedData: {self.value_type.value} is not a Function.")
        return value

    def call_value(self, current_stack: "Stack", *args: Any):
        """
        Call the wrapped data as a function.
        """
        if self.value_type != WrappedDataType.FUNCTION:
            raise TypeError(f"WrappedData: {self.value_type.value} is not callable.")

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
                st.env.var.new_var(name, args[count])

            compiled = st.run()

        return compiled
