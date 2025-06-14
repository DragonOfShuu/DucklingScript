from typing import TYPE_CHECKING, Any
from enum import Enum

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
        class Null:
            pass
        
        returnable = Null()
        if self.value_type == WrappedDataType.USER_VAR:
            returnable = self.environment.var.user_vars.get(self.key, Null())
        elif self.value_type == WrappedDataType.FUNCTION:
            returnable = self.environment.var.functions.get(self.key, Null())

        if isinstance(returnable, Null):
            raise ValueError(f"WrappedData: {self.value_type.value} with key '{self.key}' does not exist in the environment.")
        
        return returnable

    def call_value(self, current_stack: "Stack", *args: Any):
        """
        Call the wrapped data as a function.
        """
        raise NotImplementedError("Subclasses must implement this method.")
