from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, Iterable, Literal
import re

from ..pre_line import PreLine

from ..errors import InvalidSourceMapError, StackTraceNode

from .base64vlq import vlq_decode, vlq_encode

if TYPE_CHECKING:
    from ..compiled_ducky import CompiledDucky

SOURCEMAP_VERSION: Final[int] = 1

Source = tuple[int, int, int]
Mappings = list[Source]


@dataclass
class SourceMap:
    version: int
    sources: list[Path]
    mappings: list[str]

    @classmethod
    def create_sourcemap(cls, compiled: "CompiledDucky", file_sources: list[Path]):
        mappings: list[str] = []
        previous_mappings: Mappings = []
        for line in compiled:
            if line.ducky_line.strip() == "":
                mappings.append("")
                continue
            combined_mappings = line.current_stack_lines
            combined_mappings.append(
                (
                    line.pre_line.file_index,
                    line.pre_line.number,
                    -1 if line.pre_line_2 is None else line.pre_line_2.number,
                )
            )

            intersect_count, optimized = cls._optimize_mappings(
                previous_mappings, combined_mappings
            )
            if intersect_count is True:
                mappings.append("@")
                continue

            at_prefix = "" if not intersect_count else f"@{intersect_count}@"
            mappings.append(at_prefix + "".join([vlq_encode(*i) for i in optimized]))

            previous_mappings = combined_mappings
        return SourceMap(SOURCEMAP_VERSION, file_sources, mappings)

    @classmethod
    def _optimize_mappings(
        cls, previous_mappings: Mappings, new_mappings: Mappings
    ) -> tuple[Literal[True], Mappings] | tuple[int, Mappings]:
        """
        Optimize the mappings by finding
        the intersecting characters at
        the beginning of the list.

        Ex:
        previous = [(1, 2, 3), (4, 5, 6)]
        new_mapp = [(1, 2, 3), (7, 8, 9)]

        Returns:
        1, [(7, 8, 9)]

        This is because there is one intersection
        at the beginning of the numbers.
        """
        inter_count = cls._find_starting_intersection(previous_mappings, new_mappings)
        optimized = new_mappings[inter_count:]

        # This means that the last mappings
        # and these mappings are completely
        # the same
        if not optimized:
            return True, optimized

        return inter_count, optimized

    @staticmethod
    def _find_starting_intersection(list1: list[Any], list2: list[Any]):
        count = 0
        for index, item in enumerate(list1):
            if item != list2[index]:
                break
            count += 1
        return count

    def get_stacktrace_from(self, line_num: int) -> list[StackTraceNode]:
        curr_line_index = line_num - 1
        curr_mapping = self.mappings[curr_line_index]

        # Go back lines until the current line is not a @
        while curr_mapping == "@":
            curr_line_index -= 1
            if curr_line_index < 0:
                raise InvalidSourceMapError(
                    "SourceMap contained an '@' with no stack trace before it."
                )
            curr_mapping = self.mappings[curr_line_index]

        remaining_stack = self.get_stack_count(curr_mapping)
        collected: list[int] = list(
            vlq_decode(curr_mapping.removeprefix(f"@{remaining_stack}@"))
        )
        while remaining_stack:
            curr_line_index -= 1
            curr_mapping = self.mappings[curr_line_index]
            new_remaining = self.get_stack_count(curr_mapping)
            if new_remaining == remaining_stack:
                continue
            collectable_count = remaining_stack - new_remaining
            stacks = vlq_decode(curr_mapping.removeprefix(f"@{new_remaining}@"))
            collected = [*stacks[:collectable_count], *collected]

        return [
            self._to_stacktrace(stackable)
            for stackable in self._create_mappings(collected)
        ]

    def _to_stacktrace(self, source: Source):
        line1, line2 = self._to_preline(source)
        return StackTraceNode(self.convert_index_to_path(source[0]), line1, line2)

    def _to_preline(self, source: Source) -> tuple[PreLine, PreLine | None]:
        file_path = self.convert_index_to_path(source[0])
        with file_path.open() as f:
            lines = f.readlines()
            line = lines[source[1] - 1]
            line2 = None
            if source[2] != -1:
                line2 = lines[source[2] - 1]
        return PreLine(line, source[1], source[0]), None if line2 is None else PreLine(
            line2, source[2], source[0]
        )

    def _create_mappings(self, values: Iterable[int]) -> Mappings:
        """
        Convert one-dimensional list of
        file, line, and line2's into a
        two-dimensional list of mappings.
        """
        total = []
        built = []
        for count, i in enumerate(values):
            built.append(i)
            if (count + 1) % 4 == 0:
                total.append(tuple(built))
                built = []
        total.append(tuple(built))
        return total

    def convert_index_to_path(self, index: int):
        return self.sources[index]

    def get_stack_count(self, mapping: str) -> int:
        """
        Get the amount of obscured stacks.

        Obscured = Stacks at the beginning of the
        string that are not explicitly listed,
        but are numbered by the number in between
        the @'s (@4@ == 4)

        "@4@AFMAFN" # Returns 4, as there are 4 obscured stacks
        """
        matched = re.match("@(\\d)@", mapping)
        if matched is None:
            return 0
        return int(matched.groups()[0])

    def to_dict(self):
        return {
            "version": self.version,
            "sources": [str(source) for source in self.sources],
            "mappings": ",".join(self.mappings),
        }
