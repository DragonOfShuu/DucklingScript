from ..errors import VarIsNonExistentError
from .wrapped_data import WrappedData, WrappedDataType

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .environment import Environment


class WrappedVariable(WrappedData):
    """
    A class to wrap a variable in the environment.
    This allows the variable to be accessed and modified.
    """

    def __init__(self, environment: "Environment", name: str):
        super().__init__(environment, WrappedDataType.USER_VAR, name)

    @property
    def value(self) -> Any:
        try:
            return self.environment.var.get_user_var(self._value)
        except VarIsNonExistentError:
            raise VarIsNonExistentError(
                self.environment.stack,
                f"Variable '{self._value}' does not exist in the originating environment.",
            )
