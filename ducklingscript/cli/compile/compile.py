from dataclasses import dataclass
from typing import Tuple
from .pre_line import PreLine

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

    if tab_char!=None and i.startswith(tab_char): return True
    elif tab_char!=None and i[0].isspace(): raise CompilationError(f"Tab is not equivalent to the others on line {line}")
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
    def _convert_to_list(text: list[str], tab_character: str|None=None, line_num_offset: int = 0) -> list[PreLine|list]:
        tab_char: str|None = tab_character
        new_convertible = [] # In case a new list has to be created
        returnable: list[PreLine|list] = [] # A new returnable list
        line_num: int = 0
        for count,line in enumerate(text):
            line_num = count+line_num_offset+1
            if line.strip()=="": continue
            # print(f"The Line Number is: {line_num}, and the content is: {line}")

            tab = has_tab(line, tab_char, line_num)
            
            if tab==True or isinstance(tab, str):
                if isinstance(tab, str): tab_char = tab
                if tab_char==None: raise CompilationError("An error has occurred involving tabs. This error should be impossible.") 
                new_convertible.append(line.removeprefix(tab_char))
                continue
            
            if new_convertible:
                # The line number we are on now (after the tab) minus the whole block before.
                # This would give us the first line of the block, however we need to go up
                # one more because this function adds on a one already.
                returnable.append(Compile._convert_to_list(new_convertible, tab_char, line_num-len(new_convertible)-1))
                new_convertible = []
            returnable.append(PreLine(line, line_num))

        if new_convertible: returnable.append(Compile._convert_to_list(new_convertible, tab_char, line_num-len(new_convertible)-1))
        return returnable

    def parse(self, text: str):
        lines = text.split('\n')
        parsed = Compile._convert_to_list(lines)
        # compiled = 

        return parsed