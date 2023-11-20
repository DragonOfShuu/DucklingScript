from .errors import InvalidTab, UnclosedQuotations
from .pre_line import PreLine


def discover_tab_char(text: str) -> str:
    new_char = ""
    for i in text:
        if i.isspace():
            new_char += i
        else:
            return new_char
    # This should never have to be reached
    return ""


def has_tab(i: str, tab_char: str | None, line: int) -> bool | str:
    if tab_char != None and i.startswith(tab_char):
        return True
    elif tab_char != None and i[0].isspace():
        raise InvalidTab(f"Tab is not equivalent to the others on line {line}")
    else:
        if i.startswith(" ") or i.startswith("\t"):
            return discover_tab_char(i)
    return False


def parse_document(
    text: list[PreLine], tab_character: str | None = None
) -> list[PreLine | list]:
    tab_char: str | None = tab_character
    new_convertible: list[PreLine] = []  # In case a new list has to be created
    returnable: list[PreLine | list] = []  # A new returnable list
    free_tab_mode: int = 0 # Contains the line number free tab was started on

    for count, line in enumerate(text):
        if line.content.strip() == "":
            continue

        if line.content.startswith('"""') and (count == 0 or free_tab_mode):
            if free_tab_mode == 0:
                free_tab_mode = line.number
            else:
                free_tab_mode = 0
            continue

        if free_tab_mode:
            returnable.append(line)
            continue

        tab = has_tab(line.content, tab_char, line.number)

        if tab == True or isinstance(tab, str):
            if count == 0:
                raise InvalidTab(f"Unexpected tab on line {line.number}")
            if isinstance(tab, str):
                tab_char = tab
            if tab_char == None:
                raise InvalidTab(
                    "An error has occurred involving tabs. This error should be impossible."
                )
            new_line = line.content.removeprefix(tab_char)
            new_convertible.append(PreLine(new_line, line.number))
            continue

        if new_convertible:
            # The line number we are on now (after the tab) minus the whole block before.
            # This would give us the first line of the block, however we need to go up
            # one more because this function adds on a one already.
            returnable.append(parse_document(new_convertible, tab_char))
            new_convertible = []
        returnable.append(line)

    if free_tab_mode:
        raise UnclosedQuotations(f"Quotations must be closed (quotation began on {free_tab_mode})")
    if new_convertible:
        returnable.append(parse_document(new_convertible, tab_char))
    return returnable
