from typing import Any
from ducklingscript.cli.compiler.pre_line import PreLine
from .base_command import BaseCommand

parameters = [
    "END", "ESC", "ESCAPE", "SPACE", "TAB"
]
parameters.extend(f"F{range(1, 13)}")

class Alt(BaseCommand):
    names = ["SHIFT"]
    should_have_args = False

    @staticmethod
    def verify_arg(i: str) -> str | None:
        if i.upper() in parameters: return None
        elif len(i)==1: return None
        else:
            return f"Legal parameters are either a single character, or one of these: {', '.join(parameters)}"
        # return None if i.upper() in parameters else f"Improper argument. Allowed options are: {', '.join(parameters)}."
    
    @classmethod
    def run_compile(cls, commandName: PreLine, argument: str | None, code_block: list[PreLine] | None, all_args: list[str], stack: Any) -> list[str] | None:
        return (
            [f"{commandName.content.upper()} {i.upper() if i.upper() in parameters else i}" for i in all_args]
        )