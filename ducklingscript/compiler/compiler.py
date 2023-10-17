from pathlib import Path
from .pre_line import PreLine
from .stack import Stack
from .compile_options import CompileOptions
from .tab_parse import parse_document
from dataclasses import dataclass
from .errors import WarningsObject


@dataclass
class Compiled:
    output: list[str]
    warnings: WarningsObject


class Compiler:
    def __init__(self, options: CompileOptions | None = None):
        self.compile_options = options

    def compile_file(self, file: str | Path):
        '''
        Compile the given file.
        '''
        file_path = Path(file)
        if not file_path.exists():
            raise FileNotFoundError(f"The file {file} does not exist.")
        if not file_path.is_absolute():
            file_path = file_path.absolute()
        with open(file_path) as f:
            text = f.read()
        return self.compile(text, file_path)

    def compile(
        self,
        text: str | list[str],
        file: Path | None = None,
    ):
        '''
        Compile the given text.
        '''
        if isinstance(text, str):
            lines = text.split("\n")
        else:
            lines = text
        parsed = parse_document(PreLine.convert_to(lines))
        base_stack = Stack(parsed, file, compile_options=self.compile_options)

        returnable = base_stack.run()

        # return (returnable, base_stack.warnings)
        return Compiled(returnable, base_stack.warnings)
