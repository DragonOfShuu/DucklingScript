from dataclasses import dataclass
from typing import Tuple

@dataclass
class ParserOptions:
    pass

@dataclass
class ParserReturn:
    ducky: str
    newLine: int


def discover_tab_char(text: str) -> str:
    new_char = ""
    for i in text:
        if i.isspace(): new_char+=i
        else: return new_char
    # This should never have to be reached
    return ""


def has_tab(i: str, tab_char: str|None) -> bool|str:
    if tab_char and i.startswith(tab_char): return True
    else:
        if i.startswith(" ") or i.startswith("\t"): return discover_tab_char(i)
    return False


class Compile:
    def __init__(self, options: ParserOptions|None=None):
        if options==None:
            self.parser_options = ParserOptions()
        else:
            self.parser_options = options


    @staticmethod
    def _convert_to_list(text: list[str], tab_character: str|None=None) -> list[str]:
        tab_char: str|None = None
        new_convertible = [] # In case a new list has to be created
        returnable = [] # A new returnable list
        for i in text:
            if i.strip()=="": continue

            tab = has_tab(i, tab_char)
            
            if tab==True or isinstance(tab, str):
                if isinstance(tab, str): tab_char = tab
                if tab_char==None: raise TypeError("An error has occurred involving tabs. This error should be impossible.") 
                new_convertible.append(i.removeprefix(tab_char))
                continue
            
            if new_convertible:
                returnable.append(Compile._convert_to_list(new_convertible))
                new_convertible = []
            returnable.append(i)

        if new_convertible: returnable.append(Compile._convert_to_list(new_convertible))
        return returnable

    def parse(self, text: str):
        lines = text.split('\n')
        parsed = Compile._convert_to_list(lines)

        return parsed