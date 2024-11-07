from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Final

from .base64vlq import vlq_encode

if TYPE_CHECKING:
    from ..compiled_ducky import CompiledDucky

SOURCEMAP_VERSION: Final[int] = 1

@dataclass
class SourceMap:
    version: int
    sources: list[Path]
    mappings: list[str]

    @classmethod
    def create_sourcemap(cls, compiled: "CompiledDucky", file_sources: list[Path]):
        mappings: list[str] = []
        for line in compiled:
            if line.ducky_line.strip() == "":
                mappings.append('')
                continue
            mapping = (line.pre_line.file_index, line.pre_line.number, -1 if line.pre_line_2 is None else line.pre_line_2.number)
            mappings.append(vlq_encode(*mapping))
        return SourceMap(SOURCEMAP_VERSION, file_sources, mappings)

    def to_dict(self):
        return {
            "version": self.version,
            "sources": [str(source) for source in self.sources],
            "mappings": ",".join(self.mappings)
        }