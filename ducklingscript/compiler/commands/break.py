from ducklingscript.compiler.pre_line import PreLine
from .base_command import BaseCommand
from ..stack_return import StackReturn


class Break(BaseCommand):
    names = ["BREAK"]
    can_have_arguments = False

    def run_compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        all_args: list[str],
    ) -> StackReturn:
        return StackReturn.BREAK
