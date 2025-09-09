from __future__ import annotations

from typing import Protocol


class WrappedType(Protocol):
    @property
    def value(self) -> TokenValueTypes: ...


TokenValueTypes = (
    str | int | float | bool | list | dict[str, "WrappedType"]
)
"""
Types that are accepted as values for variables in DucklingScript.
"""

UnwrappedTokenValueTypes = (
    str | int | float | bool | list | dict[str, "UnwrappedTokenValueTypes"]
)
"""
Just like TokenValueTypes but where dictionaries contain unwrapped values.
"""
