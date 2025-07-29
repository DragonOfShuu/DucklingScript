from dataclasses import dataclass
from typing import Generator, Iterable, Iterator, TypeVar, cast
import re

from .errors import InvalidTabError, UnclosedQuotationsError
from .pre_line import PreLine, DimensionalPreLine


def has_tab(i: str, tab_char: str | None, line: int) -> int | str:
    """
    Returns true if the line
    has the tab given, or returns the
    tab char(s) found.
    """
    if tab_char is not None and (found:=re.match(f"{tab_char}+", i)):
        return found.group(0).count(tab_char)
    
    if tab_char is not None and re.match(r"\s", i):
        raise InvalidTabError(f"Tab is not equivalent to the others on line {line}")
    
    if discovered_tab := re.match(r"\s+", i):
        return discovered_tab.group(0)
    
    return False


# def _get_free_tab(line: PreLine, first_line: bool, gen: Iterator[PreLine]) -> tuple[list[PreLine], bool, PreLine|None]:
#     """
#     Detects if this line is a free tab,
#     and will forward the generator until 
#     the end of the free tab.

#     After in which it will return the free tab,
#     and the current value
#     """
#     content = line.content.strip()
#     if not content.startswith('"""') or not first_line: 
#         return [], first_line, line

#     free_tab: list[PreLine] = []
#     next_line = next(gen, None)
#     while next_line and next_line.content.strip() != '\"\"\"':
#         free_tab.append(next_line)
#         next_line = next(gen, None)

#     if next_line is None:
#         raise UnclosedQuotationsError(
#             f"Unclosed quotations on line {line.number}. Please ensure that all quotations are closed."
#         )

#     return free_tab, False, next(gen, None)


# def _get_new_indents(line: PreLine, tab_char: str|None, first_line: bool, gen: Iterator[PreLine]) -> tuple[list[PreLine | list], bool, PreLine|None, str|None]:
#     new_tabbed_list = []
#     current_line: PreLine|None = line

#     while current_line is not None and (tab := has_tab(current_line.content, tab_char, current_line.number)):
#         if current_line.content.strip() == "":
#             current_line = next(gen, None)
#             continue
        
#         if first_line:
#             raise InvalidTabError(f"Unexpected tab on line {current_line.number}")
        
#         if isinstance(tab, str):
#             tab_char = tab
        
#         new_tab_char = cast(str, tab_char)
        
#         new_line = current_line.content.removeprefix(new_tab_char)
#         new_tabbed_list.append(PreLine(new_line, current_line.number, current_line.file_index))
#         current_line = next(gen, None)
    
#     return parse_document(new_tabbed_list, tab_char), first_line, current_line, tab_char


@dataclass
class DocumentParserNextOptions:
    consume_new_tabs = False
    skip_empty_lines = True


class DocumentParser:
    def __init__(self, text: list[PreLine]):
        self._value = text
        # self.tabination_index = 0
        self.result_list = []
        # A stack trace of our current lists we are working
        self.current_stack = [self.result_list]
        self.iterable = iter(text)
        self._tab_char: str|None = None
    
    @property 
    def tab_char(self):
        if self._tab_char is None:
            raise ValueError("Tab character has not been instantiated, yet has been called upon.")
        return self._tab_char
    
    @tab_char.setter
    def tab_char(self, value: str):
        self._tab_char = value
        return value

    def _mutate_preline(self, preline: PreLine, content: str):
        preline.content = content
        return preline

    def add_line(self, line: PreLine):
        self.current_stack[-1].append(line)
        return line

    def next(self, options: DocumentParserNextOptions = DocumentParserNextOptions()) -> PreLine|None:
        while True:
            next_line = next(self.iterable, None)
            if next_line is None:
                return None
            
            if next_line.content.strip() == "":
                if not options.skip_empty_lines:
                    return self._mutate_preline(next_line, "")
                continue

            tab = has_tab(next_line.content, self._tab_char, next_line.number)

            if not tab:
                return next_line
            
            current_tabination = len(self.current_stack) - 1
            new_tabination = current_tabination
            if isinstance(tab, str):
                self._tab_char = tab
            elif isinstance(tab, int):
                new_tabination = tab

            if new_tabination > current_tabination+1:
                raise InvalidTabError(f"Unexpected tab on line {next_line.number}")
            
            if new_tabination > current_tabination:
                latest_item = self.current_stack[-1]
                new_list = []
                latest_item.append(new_list)
                self.current_stack.append(new_list)

def parse_document(
    text: list[PreLine], tab_character: str | None = None
) -> DimensionalPreLine:
    """
    Converts a 1-dimensional list of PreLines
    into a multidimensional list of PreLines,
    determined by the amount of tabs at the
    beginning of each line.

    Ex:
    ```
    line1
    -> line2
    -> -> line3
    -> line4
    ```
    Output
    ```
    [
        "line1",
        [
            "line2",
            [
                "line3"
            ]
            "line4"
        ]
    ]
    ```
    """
    # tab_char: str | None = tab_character
    # returnable: list[PreLine | list] = []
    # first_line = None

    # gen = iter(text)

    # for line in gen:
    #     if line.content.strip() == "":
    #         continue
        
    #     first_line = True if first_line is None else False

    #     appendable, first_line, line = _get_free_tab(line, first_line, gen)
    #     returnable.extend(appendable)
    #     # If the lines were cleared out by free tab, break out of iter
    #     if line is None: 
    #         break

    #     if line.content.strip() == "":
    #         continue

    #     appendable, first_line, line, tab_char = _get_new_indents(line, tab_char, first_line, gen)
    #     returnable.extend(appendable)
    #     if line is None:
    #         break

    #     returnable.append(line)
    # #     tab = has_tab(line.content, tab_char, line.number)

    # #     if tab or isinstance(tab, str):
    # #         if first_line:
    # #             raise InvalidTabError(f"Unexpected tab on line {line.number}")
    # #         if isinstance(tab, str):
    # #             tab_char = tab
    # #         if tab_char is None:
    # #             raise InvalidTabError(
    # #                 "An error has occurred involving tabs. This error should be impossible."
    # #             )
    # #         new_line = line.content.removeprefix(tab_char)
    # #         new_convertible.append(PreLine(new_line, line.number, line.file_index))
    # #         continue

    # #     if new_convertible:
    # #         returnable.append(parse_document(new_convertible, tab_char))
    # #         new_convertible = []
    # #     returnable.append(line)

    # # if new_convertible:
    # #     returnable.append(parse_document(new_convertible, tab_char))
    # return returnable
