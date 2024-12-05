from __future__ import annotations

from abc import ABC, abstractmethod

from dataclasses import dataclass
from enum import Enum
from typing import NotRequired, TypedDict


class ArgReqType(Enum):
    """
    Argument requirement type,
    whether the argument is
    `REQUIRED`, `ALLOWED`, OR
    `NOTALLOWED`.
    """

    REQUIRED = 0
    """
    The argument is required
    for the command to run.
    """
    ALLOWED = 1
    """
    The argument is accepted,
    but not necessary.
    """
    NOTALLOWED = 2
    """
    The argument is not 
    acceptable.
    """


@dataclass
class Example:
    class ExampleDict(TypedDict):
        duckling: str
        compiled: NotRequired[str]
        std_out: NotRequired[str]
        file_structure: NotRequired[dict[str, None | dict]]

    duckling: str
    compiled: str | None = None
    std_out: str | None = None
    file_structure: dict[str, None | dict] | None = None

    @staticmethod
    def from_dict(obj: ExampleDict) -> Example:
        return Example(**obj)


@dataclass
class ComDoc:
    names: list[str]
    flipper_only: bool
    quackinter_only: bool
    argument_type: type | str
    arg_req_type: ArgReqType
    parameters: list[str] | None
    description: str
    examples: list[Example] | None


class DocCommand(ABC):
    """
    A class for making Documentation
    inside of commands.
    """
    description: str = "[No Description Provided]"
    """
    Description of this command
    """
    parameters: list[str] | None = None
    """
    Possible parameters for this
    command.

    THIS VARIABLE IS FOR STYLE ONLY,
    AND DOES NOT DO ANYTHING EXCEPT
    PROVIDE DOCUMENTATION.
    """
    examples: list[Example] | None = None
    flipper_only: bool = False
    """
    If this command is only supported for
    the Flipper Zero's version of 
    duckyscript.
    """
    quackinter_only: bool = False
    """
    If the command is only supported for
    the Quackinter interpeter built
    into DucklingScript
    """

    @classmethod
    @abstractmethod
    def get_doc(cls) -> ComDoc:
        pass
