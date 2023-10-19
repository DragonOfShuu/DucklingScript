from typing import Any
from ..pre_line import PreLine
from .base_command import BaseCommand

parameters = ["BREAK", "PAUSE", "ESCAPE", "ESC"]
parameters.extend([f"F{num}" for num in range(1, 13)])


class Ctrl(BaseCommand):
    names = ["CTRL", "CONTROL"]
    should_have_args = False

    def verify_arg(self, i: str) -> str | None:
        if i.upper() in parameters:
            return None
        elif len(i) == 1:
            return None
        else:
            return f"'{i}' is not an acceptable arg. Legal parameters are either a single character, or one of these: {', '.join(parameters)}"

    def run_compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        all_args: list[str],
    ) -> list[str] | None:
        return [
            f"{commandName.content.upper()} {i.upper() if i.upper() in parameters else i}"
            for i in all_args
        ]
