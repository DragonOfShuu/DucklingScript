from .bases.doc_command import ArgReqType
from ducklingscript.compiler.commands.bases.simple_command import ArgLine
from ducklingscript.compiler.compiled_ducky import CompiledDucky
from ducklingscript.compiler.pre_line import PreLine
from .bases.simple_command import SimpleCommand

desc = """
Expresses a variable/function
to the environment, thus when the
file is imported with that environment,
the exported items are what's imported.
"""

class Export(SimpleCommand):
    names = ["EXPORT"]
    description = desc
    arg_req = ArgReqType.REQUIRED

    def run_compile(self, command_name: PreLine, arg: ArgLine) -> str | list[str] | None | CompiledDucky:
        arg_content: str = arg.content
        exportable = [i.strip() for i in arg_content.split(",")]
        for var_name in exportable:
            self.env.var.express_var(var_name)
        return None
