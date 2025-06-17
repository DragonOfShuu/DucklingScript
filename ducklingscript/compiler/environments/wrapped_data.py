from typing import TYPE_CHECKING, Any
from enum import Enum

from ..errors import InvalidArgumentsError

if TYPE_CHECKING:
    from .environment import Environment
    from ..stack import Stack

class WrappedDataType(Enum):
    USER_VAR = "user_var"
    FUNCTION = "function"

class WrappedData():
    """
    A base class for wrapped data types
    """
    ...  # This class is intentionally left empty as a base class for other wrapped data types.
    def __init__(self, environment: "Environment", value_type: WrappedDataType, key: str):
        self.environment = environment
        self.value_type = value_type
        self.key = key

    def get_value(self):
        """
        Get the value of the wrapped data.
        This method should be implemented by subclasses.
        """
        if self.value_type == WrappedDataType.USER_VAR and self.key in self.environment.var.user_vars:
            return self.environment.var.user_vars[self.key]

        if self.value_type == WrappedDataType.FUNCTION and self.key in self.environment.var.functions:
            return self.environment.var.functions[self.key]

        raise ValueError(f"WrappedData: Unknown value_type '{self.value_type}' for key '{self.key}'.")

    def call_value(self, current_stack: "Stack", *args: Any):
        """
        Call the wrapped data as a function.
        """
        if self.value_type != WrappedDataType.FUNCTION:
            raise TypeError(f"WrappedData: {self.value_type.value} with key '{self.key}' is not callable.")
        
        function = self.get_value()

        stack_pile = current_stack.stack_pile

        if len(function.arguments) != len(args):
            raise InvalidArgumentsError(
                current_stack,
                f"{len(args)} arguments were given when {len(function.arguments)} was expected.",
            )

        with stack_pile.add_stack_above(function.code, function.file, injectable_env=self.environment) as st:
            for count, name in enumerate(function.arguments):
                st.env.var.new_var(name, args[count])

            compiled = st.run()

        return compiled
    