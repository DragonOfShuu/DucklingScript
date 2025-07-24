from .bases.doc_command import ArgReqType
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.compiled_ducky import CompiledDucky
from .bases import ArgLine, SimpleCommand
from ..tokenization import Tokenizer

desc = """
Defines a new variable. Give the name, then the value, separated by a space.

`VAR` is used when you want to create a variable. If the variable already exists, it will be edited.
`LOCALVAR` is used when you want to create a variable that is only available in the current 
environment (and also accessible in child environments).
"""


class Var(SimpleCommand):
    names = ["VAR", "LOCALVAR"]
    arg_req = ArgReqType.REQUIRED
    arg_type = "<name> <value>"

    description = desc

    def verify_arg(self, arg: ArgLine) -> str | None:
        arg = arg.content.strip().split(maxsplit=1)
        if len(arg) != 2:
            return "The syntax for creating a var goes as follows: VAR <name> <value>"

    def run_compile(
        self, command_name: PreLine, arg: ArgLine
    ) -> str | list[str] | CompiledDucky | None:
        name = command_name.content_as_upper()
        var_name, value = arg.content.split(maxsplit=1)

        if name == "VAR":
            self.env.var.new_user_var(
                var_name, Tokenizer.tokenize(value, self.stack, self.env)
            )
        
        elif name == "LOCALVAR":
            self.env.var.hard_new_var(
                var_name, Tokenizer.tokenize(value, self.stack, self.env)
            )
