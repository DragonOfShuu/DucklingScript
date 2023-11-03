from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path

from .pre_line import PreLine
from .tokenization import token_return_types


class StackReturnType(Enum):
    NORMAL = 0
    RETURN = 1
    BREAK = 2
    CONTINUE = 3


@dataclass
class StdOutData:
    line: PreLine
    file: Path | None


@dataclass
class CompiledReturn:
    data: list[str] = field(default_factory=list)
    return_type: StackReturnType = StackReturnType.NORMAL
    return_data: token_return_types | None = None
    std_out: list[StdOutData] = field(default_factory=list)

    def append(self, x: CompiledReturn):
        self.data.extend(x.data)
        self.return_type = x.return_type
        self.return_data = x.return_data
        # self.std_out.extend(x.std_out)

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

    def add_to_std(self, x: StdOutData):
        self.std_out.append(x)


@dataclass
class BaseReturn:
    output: list[str]
    std_out: list[StdOutData]
