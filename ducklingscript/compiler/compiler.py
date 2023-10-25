from pathlib import Path
from .pre_line import PreLine
from .stack import Stack
from .compile_options import CompileOptions
from .tab_parse import parse_document
from dataclasses import dataclass
from .errors import WarningsObject
from .environment import Environment


@dataclass
class Compiled:
    output: list[str]
    warnings: WarningsObject
    env: Environment


class Compiler:
    def __init__(self, options: CompileOptions | None = None):
        self.compile_options = options

    @staticmethod
    def prepare_for_stack(lines: list, skip_indentation: bool = False):
        if not skip_indentation:
            return parse_document(PreLine.convert_to(lines))
        else:
            return PreLine.convert_to_recur(lines)

    def compile_file(self, file: str | Path):
        """
        Compile the given file.
        """
        file_path = Path(file)
        if not file_path.exists():
            raise FileNotFoundError(f"The file {file} does not exist.")
        if not file_path.is_absolute():
            file_path = file_path.absolute()
        with open(file_path) as f:
            text = f.read()
        return self.compile(text, file_path)

    def compile(
        self, text: str | list, file: Path | None = None, skip_indentation: bool = False
    ):
        """
        Compile the given text.
        """
        if isinstance(text, str):
            lines = text.split("\n")
        else:
            lines = text

        # parsed = lines
        parsed = self.prepare_for_stack(lines, skip_indentation)

        base_stack = Stack(parsed, file, compile_options=self.compile_options)

        returnable = base_stack.start_base()

        # return (returnable, base_stack.warnings)
        return Compiled(returnable, base_stack.warnings, base_stack.env)
