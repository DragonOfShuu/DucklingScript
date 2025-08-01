from __future__ import annotations

from dataclasses import dataclass
import re
from typing import NoReturn

from .errors import InvalidTabError, UnclosedQuotationsError
from .pre_line import PreLine, DimensionalPreLine


@dataclass
class DocumentParserNextOptions:
    consume_new_tabs: bool = True
    skip_empty_lines: bool = True


def has_tab(i: str, tab_char: str | None, line: int) -> int | str:
    """
    Returns true if the line
    has the tab given, or returns the
    tab char(s) found.
    """ 
    if tab_char is not None:
        found_tabs = re.match(f"{tab_char}+", i)
        tab_prefix = found_tabs.group(0) if found_tabs else ""
        if re.match(r'\s', i.removeprefix(tab_prefix)):
            raise InvalidTabError(f"Tab is not equivalent to the others on line {line}")
        elif not found_tabs:
            return 0
        return found_tabs.group(0).count(tab_char)
    
    if discovered_tab := re.match(r"\s+", i):
        return discovered_tab.group(0)
    
    return 0


def _get_free_tab(line: PreLine, gen: DocumentParser) -> PreLine|None:
    """
    Detects if this line is a free tab,
    and will forward the generator until 
    the end of the free tab.

    After in which it will return the free tab,
    and the current value
    """
    first_line = not gen.current_stack[-1]

    content = line.content.strip()
    if not content.startswith('"""') or not first_line: 
        return line

    # free_tab: list[PreLine] = []
    options = DocumentParserNextOptions(False, False)
    next_line = gen.next(options)
    while next_line and next_line.content.strip() != '\"\"\"':
        # free_tab.append(next_line)
        next_line = gen.add_line(next_line)

    if next_line is None:
        raise UnclosedQuotationsError(
            f"Unclosed quotations on line {line.number}. Please ensure that all quotations are closed."
        )

    return gen.next()

class DocumentParser:
    def __init__(self, text: list[PreLine]):
        self._value = text
        # self.tabination_index = 0
        self.result_list: DimensionalPreLine = []
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
    
    @property
    def tabination_index(self):
        return len(self.current_stack) - 1

    def _mutate_preline(self, preline: PreLine, content: str):
        return PreLine(content, preline.number, preline.file_index)

    def add_line(self, line: PreLine):
        self.current_stack[-1].append(line)
        return line
    

    def _remove_tabs(self, line: PreLine, check_tabs: bool = True, tab_count_override: int|None = None):
        if not re.match(r'\s', line.content):
            return PreLine(line.content, line.number, line.file_index)
        
        tab_amount = tab_count_override if tab_count_override is not None else self.tabination_index
        content = line.content
        matched_content = re.match(f"({self.tab_char}){{{tab_amount}}}", content)

        if not matched_content:
            return PreLine(line.content, line.number, line.file_index)
        
        content = content.removeprefix(matched_content.group(0))
        return PreLine(content, line.number, line.file_index)

    def next(self, options: DocumentParserNextOptions = DocumentParserNextOptions()) -> PreLine|None:
        while True:
            next_line = next(self.iterable, None)
            if next_line is None:
                return None
            
            if next_line.content.strip() == "":
                if not options.skip_empty_lines:
                    return self._remove_tabs(self._mutate_preline(next_line, ""))
                continue

            tab = has_tab(next_line.content, self._tab_char, next_line.number)
            
            current_tabination = len(self.current_stack) - 1
            new_tabination = current_tabination
            if isinstance(tab, str):
                self._tab_char = tab
                new_tabination += 1
            elif isinstance(tab, int):
                new_tabination = tab

            if (not options.consume_new_tabs) and new_tabination >= current_tabination:
                return self._remove_tabs(next_line)

            if new_tabination > current_tabination+1:
                raise InvalidTabError(f"Unexpected tab on line {next_line.number}")
            
            if new_tabination > current_tabination:
                latest_item = self.current_stack[-1]
                new_list = []
                latest_item.append(new_list)
                self.current_stack.append(new_list)
            
            elif new_tabination < current_tabination:
                self.current_stack = self.current_stack[:new_tabination+1]
            
            return self._remove_tabs(next_line)


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
    parser = DocumentParser(text)
    while current_line := parser.next():
        next_line = _get_free_tab(current_line, parser)
        if not next_line:
            continue

        parser.add_line(next_line)
    
    return parser.result_list
