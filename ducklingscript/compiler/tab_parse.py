from .errors import InvalidTabError, UnclosedQuotationsError
from .pre_line import PreLine, DimensionalPreLine


def discover_tab_char(text: str) -> str:
    """
    Returns the tab character
    found at the beginning of
    the line, or an empty string
    if none was found.
    """
    new_char = ""
    for i in text:
        if i.isspace():
            new_char += i
        else:
            return new_char
    return ""


def has_tab(i: str, tab_char: str | None, line: int) -> bool | str:
    """
    Returns true if the line
    has the tab given, or returns the
    tab char(s) found.
    """
    if tab_char is not None and i.startswith(tab_char):
        return True
    elif tab_char is not None and i[0].isspace():
        raise InvalidTabError(f"Tab is not equivalent to the others on line {line}")
    else:
        if i.startswith(" ") or i.startswith("\t"):
            return discover_tab_char(i)
    return False


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
    tab_char: str | None = tab_character
    new_convertible: list[PreLine] = []  # In case a new list has to be created
    returnable: list[PreLine | list] = []  # A new returnable list
    free_tab_mode: int = 0  # Contains the line number free tab was started on

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

        if tab or isinstance(tab, str):
            if count == 0:
                raise InvalidTabError(f"Unexpected tab on line {line.number}")
            if isinstance(tab, str):
                tab_char = tab
            if tab_char is None:
                raise InvalidTabError(
                    "An error has occurred involving tabs. This error should be impossible."
                )
            new_line = line.content.removeprefix(tab_char)
            new_convertible.append(PreLine(new_line, line.number, line.file_index))
            continue

        if new_convertible:
            # The line number we are on now (after the tab) minus the whole block before.
            # This would give us the first line of the block, however we need to go up
            # one more because this function adds on a one already.
            returnable.append(parse_document(new_convertible, tab_char))
            new_convertible = []
        returnable.append(line)

    if free_tab_mode:
        raise UnclosedQuotationsError(
            f"Quotations must be closed (quotation began on {free_tab_mode})"
        )
    if new_convertible:
        returnable.append(parse_document(new_convertible, tab_char))
    return returnable
