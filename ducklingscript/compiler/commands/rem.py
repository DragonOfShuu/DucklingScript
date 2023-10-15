from ..pre_line import PreLine
from .base_command import BaseCommand


class Rem(BaseCommand):
    names = ["REM"]

    def run_compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        all_args: list[str],
    ) -> list[str] | None:
        # print(self.stack.compile_options.include_comments)
        if self.stack.compile_options.include_comments:
            return super().run_compile(commandName, argument, code_block, all_args)
        else:
            return None
