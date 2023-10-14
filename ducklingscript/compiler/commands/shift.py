from typing import Any
from ..pre_line import PreLine
from .base_command import BaseCommand


class Shift(BaseCommand):
    names = ["SHIFT"]
    should_have_args = False

    @staticmethod
    def verify_arg(i: str) -> str | None:
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

    @classmethod
    def run_compile(
        cls,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        all_args: list[str],
        stack: Any,
    ) -> list[str] | None:
        return [f"{commandName.content.upper()} {i.upper()}" for i in all_args]
