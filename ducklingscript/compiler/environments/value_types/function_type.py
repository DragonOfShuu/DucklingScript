from ...pre_line import PreLine


from dataclasses import dataclass
from pathlib import Path


@dataclass
class Function:
    name: str
    arguments: list[str]
    code: list[PreLine | list]
    file: str | Path | None
