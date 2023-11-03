from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn, StdOutData
from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand


class Print(SimpleCommand):
    names = ["PRINT"]

    def run_compile(
        self, commandName: PreLine, all_args: list[token_return_types]
    ) -> list[str] | CompiledReturn | None:
        pre_list = [PreLine(str(i), commandName.number) for i in all_args]
        return CompiledReturn(
            std_out=[StdOutData(i, self.stack.file) for i in pre_list]
        )
