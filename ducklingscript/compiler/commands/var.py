from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from .bases import SimpleCommand, ArgReqType
from ..tokenization import Tokenizer


class Var(SimpleCommand):
    names = ["VAR"]
    arg_req = ArgReqType.REQUIRED

    @staticmethod
    def verify_arg(i: str) -> str | None:
        arg = i.strip().split(maxsplit=1)
        if len(arg) != 2:
            return "The syntax for creating a var goes as follows: VAR <name> <value>"

    # def run_compile(
    #     self, commandName: PreLine, all_args: list[str]
    # ) -> list[str] | StackReturnType | None:
    def run_compile(
        self, commandName: PreLine, arg: str
    ) -> str | CompiledReturn | None:
        var_name, value = arg.split(maxsplit=1)
        self.env.new_var(var_name, Tokenizer.tokenize(value, self.stack, self.env))
