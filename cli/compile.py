from dataclasses import dataclass
from typing import Tuple

class CompilationError(Exception):
    pass

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


def has_tab(i: str, tab_char: str|None, line: int) -> bool|str:
    if isinstance(tab_char, str) and i.startswith(tab_char): return True
    elif isinstance(tab_char, str) and i[0].isspace(): raise CompilationError(f"Tab is not equivalent to the others on line {line}")
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
    def _convert_to_list(text: list[str], tab_character: str|None=None, line_num_offset: int = 0) -> list[str]:
        tab_char: str|None = tab_character
        new_convertible = [] # In case a new list has to be created
        returnable = [] # A new returnable list

        for count,i in enumerate(text):
            line: int = count+line_num_offset+1
            if i.strip()=="": continue

            tab = has_tab(i, tab_char, line)
            
            if tab==True or isinstance(tab, str):
                if isinstance(tab, str): tab_char = tab
                if tab_char==None: raise CompilationError("An error has occurred involving tabs. This error should be impossible.") 
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