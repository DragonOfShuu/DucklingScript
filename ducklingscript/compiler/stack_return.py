from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field
from .tokenization import token_return_types


class StackReturnType(Enum):
    NORMAL = 0
    RETURN = 1
    BREAK = 2
    CONTINUE = 3


@dataclass
class CompiledReturn:
    data: list[str] = field(default_factory=list)
    return_type: StackReturnType = StackReturnType.NORMAL
    return_data: token_return_types | None = None

    def append(self, x: CompiledReturn):
        self.data.extend(x.data)
        self.return_type = x.return_type
        self.return_data = x.return_data

    # Funni mathematical naming
    def normalize(self):
        self.return_type = StackReturnType.NORMAL

    def get_return(self, normalize: bool = True, reset: bool = True):
        if normalize:
            self.normalize()

        x = self.return_data

        if reset:
            self.return_data = None

        return x
