from abc import ABC, abstractclassmethod, abstractmethod


from dataclasses import dataclass
from enum import Enum


class ArgReqType(Enum):
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
class ComDoc:
    names: list[str]
    argument_type: type|str
    arg_req_type: ArgReqType
    parameters: list[str]|None
    description: str
    example_duckling: list[str]|None = None
    example_compiled: list[str]|None = None


class DocCommand(ABC):
    description: str = ''
    '''
    Description of this command
    '''
    parameters: list[str]|None = None
    '''
    Possible parameters for this
    command.

    THIS VARIABLE IS FOR STYLE ONLY,
    AND DOES NOT DO ANYTHING EXCEPT
    PROVIDE DOCUMENTATION.
    '''
    example_duckling: list[str]|None = None
    example_compiled: list[str]|None = None

    @classmethod
    @abstractmethod
    def get_doc(cls) -> ComDoc:
        pass