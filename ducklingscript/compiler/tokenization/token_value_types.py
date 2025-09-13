from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from ..pre_line import PreLine


class WrappedType(Protocol):
    @property
    def value(self) -> TokenValueTypes:
        ...


@dataclass
class Function:
    name: str
    arguments: list[str]
    code: list[PreLine | list]
    file: str | Path | None


TokenValueTypes = str | int | float | bool | list | Function | dict[str, "WrappedType"]
"""
Types that are accepted as values for variables in DucklingScript.
"""

UnwrappedTokenValueTypes = (
    str | int | float | bool | list | Function | dict[str, "UnwrappedTokenValueTypes"]
)
"""
Just like TokenValueTypes but where dictionaries contain unwrapped values.
"""
