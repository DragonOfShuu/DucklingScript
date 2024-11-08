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


FileLineLine2 = tuple[int, int, int]


@dataclass
class CompiledDuckyLine:
    pre_line: PreLine
    ducky_line: str
    pre_line_2: PreLine|None = None
    current_stack_lines: list[FileLineLine2] = field(default_factory=list)

    def __post_init__(self):
        if self.pre_line == self.pre_line_2:
            self.pre_line_2 = None


@dataclass
class CompiledDucky:
    data: list[CompiledDuckyLine] = field(default_factory=list)
    return_type: StackReturnType = StackReturnType.NORMAL
    return_data: token_return_types | None = None
    std_out: list[StdOutData] = field(default_factory=list)

    def append(self, x: CompiledDucky, include_std: bool = True):
        """
        Extend with a CompiledReturn on to this.

        WARNING: The inputted CompiledReturn will
        overwrite the return_type and return_data
        of this CompiledReturn.
        """
        self.data.extend(x.data)
        self.return_type = x.return_type
        self.return_data = x.return_data
        if include_std:
            self.std_out.extend(x.std_out)

    # Funni mathematical naming
    def normalize(self):
        """
        Set the return type
        to be NORMAL.
        """
        self.return_type = StackReturnType.NORMAL

    def get_return(self, normalize: bool = True, reset: bool = True):
        """
        Get the return data.

        Arguments:
            - Normalize: If the return type should
            be set to NORMAL.
            - Reset: If we should set the return_data
            to None.
        """
        if normalize:
            self.normalize()

        x = self.return_data

        if reset:
            self.return_data = None

        return x
    
    def add_lines(self, *lines: CompiledDuckyLine):
        self.data.extend(lines)

    def add_to_std(self, x: StdOutData):
        self.std_out.append(x)

    def get_ducky(self) -> list[str]:
        return [line.ducky_line for line in self.data]
    
    def add_stack_initator(self, line: FileLineLine2):
        """
        Add the line that initiated the code
        that got compiled from running in the
        first place.

        Often ran by the end of Stack to solidify
        the context.
        """
        for comp in self.data:
            comp.current_stack_lines.insert(0, line)

    def __iter__(self):
        for line in self.data:
            yield line
