from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand


class Pass(SimpleCommand):
    names = ["PASS"]
    can_have_arguments = False

    def run_compile(
        self, commandName: PreLine, all_args: list[token_return_types]
    ) -> list[str] | CompiledReturn | None:
        return
