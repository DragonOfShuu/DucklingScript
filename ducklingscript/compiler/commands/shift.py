from typing import Any
from ..pre_line import PreLine
from .base_command import BaseCommand


class Shift(BaseCommand):
    names = ["SHIFT"]
    should_have_args = False

    def verify_arg(self, i: str) -> str | None:
        parameters = [
            "DELETE",
            "HOME",
            "INSERT",
            "PAGEUP",
            "PAGEDOWN",
            "WINDOWS",
            "GUI",
            "UPARROW",
            "DOWNARROW",
            "LEFTARROW",
            "RIGHTARROW",
            "TAB",
        ]
        return (
            None
            if i.upper() in parameters
            else f"Improper argument. Allowed options are: {', '.join(parameters)}."
        )

    def run_compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        all_args: list[str],
    ) -> list[str] | None:
        return [f"{commandName.content.upper()} {i.upper()}" for i in all_args]
