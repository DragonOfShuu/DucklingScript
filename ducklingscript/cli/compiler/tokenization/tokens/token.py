from __future__ import annotations
from enum import Enum
from typing import Any
from abc import ABC, abstractmethod

class Token(ABC):
    class isToken(Enum):
        FALSE = 0 # Stop giving chars, and ask someone else about this char
        TRUE = 1 # Continue giving us chars
        CONTINUE = 2 # After this char you gave me switch to someone else

    def __init__(self, stack: Any):
        self.stack = stack
        self.__init_token_vars()

    @abstractmethod
    def __init_token_vars(self):
        pass
    
    @abstractmethod
    def addCharToToken(self, char: str) -> Token.isToken:
        '''
        Return False if this char
        is not relative to this
        token type.
        '''
        return self.isToken.FALSE
    
