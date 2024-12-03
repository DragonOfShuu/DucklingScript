from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from .errors import StackTraceNode

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
class CompiledStackTrace:
    line: PreLine
    line2: PreLine | None

    @property
    def coordinates(self) -> FileLineLine2:
        """
        Gives coordinates as File, Line, Line2:
        (0, 1, 1)
        """
        return (
            self.file_index,
            self.line.number,
            self.line2.number if self.line2 else -1,
        )

    @property
    def file_index(self) -> int | Literal[-1]:
        """
        Returns -1 if there is no associated
        file index, otherwise gives file 0-based
        file index.
        """
        return self.line.file_index


@dataclass
class CompiledDuckyLine:
    pre_line: PreLine
    ducky_line: str
    pre_line_2: PreLine | None = None
    lower_stack_lines: list[CompiledStackTrace] = field(default_factory=list)

    def __post_init__(self):
        if self.pre_line == self.pre_line_2:
            self.pre_line_2 = None

    @property
    def stack_trace(self) -> list[CompiledStackTrace]:
        return [
            *self.lower_stack_lines,
            CompiledStackTrace(self.pre_line, self.pre_line_2),
        ]


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
        """
        Add the StdOutData to the 
        currently stored list.
        """
        self.std_out.append(x)

    def get_ducky(self) -> list[str]:
        """
        Get stored DuckyScript lines as
        a list of strings.
        """
        return [line.ducky_line for line in self.data]

    def add_stack_initator(self, line: PreLine, line2: PreLine | None):
        """
        Add the line that initiated the code
        that got compiled from running in the
        first place.

        Often ran by the end of Stack to solidify
        the context.
        """
        stack_initiator = CompiledStackTrace(line, line2)
        for comp in self.data:
            comp.lower_stack_lines.insert(0, stack_initiator)

    def get_duckling_stacktrace(
        self, line_num: int, sources: list[Path]
    ) -> list[StackTraceNode]:
        """
        Get the stacktrace from the original
        DucklingScript based on the line number
        from the compiled.

        Arguments:
            - line_num: A **1-based** index of the line
            location
        """
        corrected_line = line_num - 1
        line_ref = self[corrected_line]
        traceback: list[StackTraceNode] = []
        for duckling_line in line_ref.stack_trace:
            traceback.append(
                StackTraceNode(
                    sources[duckling_line.file_index],
                    duckling_line.line,
                    duckling_line.line2,
                )
            )
        return traceback

    def __iter__(self):
        for line in self.data:
            yield line

    def __getitem__(self, index: int):
        """
        A 0-based get line from compiled.

        Returns
            - The requested CompiledDuckyLine
        """
        return self.data[index]

    def __len__(self):
        return self.data.__len__()
    