from .bases.doc_command import ArgReqType
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from .bases import Line, SimpleCommand
from ..tokenization import Tokenizer


class Var(SimpleCommand):
    names = ["VAR"]
    arg_req = ArgReqType.REQUIRED

    # @staticmethod
    # def verify_arg(i: str) -> str | None:
    def verify_arg(self, arg: Line) -> str | None:
        arg = arg.content.strip().split(maxsplit=1)
        if len(arg) != 2:
            return "The syntax for creating a var goes as follows: VAR <name> <value>"

    def run_compile(
        self, commandName: PreLine, arg: Line
    ) -> str | list[str] | CompiledReturn | None:
        var_name, value = arg.content.split(maxsplit=1)
        self.env.new_var(var_name, Tokenizer.tokenize(value, self.stack, self.env))
