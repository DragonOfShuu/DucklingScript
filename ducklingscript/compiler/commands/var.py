from .bases.doc_command import ArgReqType
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from .bases import Line, SimpleCommand
from ..tokenization import Tokenizer

desc = """
Defines a new variable. Give the name, then the value, separated by a space.
"""


class Var(SimpleCommand):
    names = ["VAR"]
    arg_req = ArgReqType.REQUIRED
    arg_type = "<name> <value>"

    description = desc

    def verify_arg(self, arg: Line) -> str | None:
        arg = arg.content.strip().split(maxsplit=1)
        if len(arg) != 2:
            return "The syntax for creating a var goes as follows: VAR <name> <value>"

    def run_compile(
        self, command_name: PreLine, arg: Line
    ) -> str | list[str] | CompiledReturn | None:
        var_name, value = arg.content.split(maxsplit=1)
        self.env.var.new_var(var_name, Tokenizer.tokenize(value, self.stack, self.env))
