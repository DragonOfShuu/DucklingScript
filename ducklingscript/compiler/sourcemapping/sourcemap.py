from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, Literal

from .base64vlq import vlq_encode

if TYPE_CHECKING:
    from ..compiled_ducky import CompiledDucky

SOURCEMAP_VERSION: Final[int] = 1

FileLineLine2 = tuple[int, int, int]
Mappings = list[FileLineLine2]

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

            intersect_count, optimized = cls._optimize_mappings(previous_mappings, combined_mappings)
            if intersect_count is True:
                mappings.append('@')
                continue
            
            at_prefix = "" if not intersect_count else f'@{intersect_count}@'
            mappings.append(at_prefix + "".join([vlq_encode(*i) for i in optimized]))
            
            previous_mappings = combined_mappings
        return SourceMap(SOURCEMAP_VERSION, file_sources, mappings)

    @classmethod
    def _optimize_mappings(cls, previous_mappings: Mappings, new_mappings: Mappings) -> tuple[Literal[True], Mappings] | tuple[int, Mappings]:
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
        for index,item in enumerate(list1):
            if item!=list2[index]:
                break
            count+=1
        return count

    def to_dict(self):
        return {
            "version": self.version,
            "sources": [str(source) for source in self.sources],
            "mappings": ",".join(self.mappings),
        }
