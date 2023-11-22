from .bases.doc_command import ArgReqType
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn, StdOutData
from ducklingscript.compiler.tokenization import token_return_types
from .bases import Line, SimpleCommand


class Print(SimpleCommand):
    names = ["PRINT"]

    def multi_comp(self, commandName, all_args) -> list[str] | CompiledReturn | None:
        pre_list = [PreLine(str(i), commandName.number) for i in all_args]
        return CompiledReturn(
            std_out=[StdOutData(i, self.stack.file) for i in pre_list]
        )

    # def run_compile(self, commandName: PreLine, arg: str | None) -> str | list[str] | CompiledReturn | None:
    def run_compile(self, commandName: PreLine, arg: Line | None) -> str | list[str] | CompiledReturn | None:
        if arg is None:
            return None
        
        return CompiledReturn(
            std_out=[StdOutData(PreLine(arg.content, arg.line_num), self.stack.file)]
        )