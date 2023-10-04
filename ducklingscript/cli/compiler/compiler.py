from dataclasses import dataclass
from pathlib import Path
from .pre_line import PreLine
from .stack import Stack
from .errors import CompilationError, InvalidTab


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
        raise CompilationError(f"Tab is not equivalent to the others on line {line}")
    else:
        if i.startswith(" ") or i.startswith("\t"):
            return discover_tab_char(i)
    return False


class Compiler:
    def __init__(self, options: ParserOptions | None = None):
        if options == None:
            self.parser_options = ParserOptions()
        else:
            self.parser_options = options

    @staticmethod
    def _convert_to_list(
        text: list[PreLine], tab_character: str | None = None
    ) -> list[PreLine | list]:
        tab_char: str | None = tab_character
        new_convertible: list[PreLine] = []  # In case a new list has to be created
        returnable: list[PreLine | list] = []  # A new returnable list

        for count, line in enumerate(text):
            # print(f"Line {line.number}: {line.content}")
            if line.content.strip() == "":
                continue

            tab = has_tab(line.content, tab_char, line.number)

            if tab == True or isinstance(tab, str):
                if count == 0:
                    raise InvalidTab(f"Unexpected tab on line {line.number}")
                if isinstance(tab, str):
                    tab_char = tab
                if tab_char == None:
                    raise CompilationError(
                        "An error has occurred involving tabs. This error should be impossible."
                    )
                new_line = line.content.removeprefix(tab_char)
                new_convertible.append(PreLine(new_line, line.number))
                continue

            if new_convertible:
                # The line number we are on now (after the tab) minus the whole block before.
                # This would give us the first line of the block, however we need to go up
                # one more because this function adds on a one already.
                returnable.append(Compiler._convert_to_list(new_convertible, tab_char))
                new_convertible = []
            returnable.append(line)

        # This is wrong
        if new_convertible:
            returnable.append(Compiler._convert_to_list(new_convertible, tab_char))
        return returnable

    def compile_file(self, file: str | Path):
        file_path = Path(file)
        if not file_path.exists():
            raise FileNotFoundError(f"The file {file} does not exist.")
        if not file_path.is_absolute():
            file_path = file_path.absolute()
        with open(file_path) as f:
            text = f.read()
        return self.compile(text, file_path)

    def compile(self, text: str | list[str], file: Path | None = None):
        if isinstance(text, str):
            lines = text.split("\n")
        else:
            lines = text
        parsed = Compiler._convert_to_list(PreLine.convert_to(lines))
        base_stack = Stack(parsed, file)

        returnable = base_stack.start()

        return (returnable, base_stack.warnings)
        # return compiled