from ducklingscript.compiler.commands.bases.simple_command import ArgLine
from ..environments.env_extend_type import EnvExtendType
from .utility.file_path import convert_to_path
from ducklingscript.compiler.compiled_ducky import CompiledDucky
from ..errors import NotAValidCommandError
from ducklingscript.compiler.pre_line import PreLine
from .bases.simple_command import SimpleCommand


desc = """
Import a file like it's
a module (all expressed
variables are what get imported)
"""


class Import(SimpleCommand):
    names = ["IMPORT"]
    description = desc
    arg_type = "<filePath>"

    def verify_arg(self, arg: ArgLine) -> str | None:
        if arg.content.endswith("."):
            return "The dot operator cannot appear alone at the end of path."

    def run_compile(
        self, command_name: PreLine, arg: ArgLine
    ) -> str | list[str] | None | CompiledDucky:
        from ..compiler import DucklingCompiler

        if self.stack.file is None:
            raise NotAValidCommandError(
                self.stack, "The IMPORT command cannot be used outside of a file."
            )

        file_path = convert_to_path(self.stack_pile, self.stack.file, arg.content)

        with file_path.open() as f:
            text = f.read().splitlines()

        file_index = self.env.proj.register_file(file_path)

        commands = DucklingCompiler._prepare_for_stack(text, file_index)

        with self.stack_pile.add_stack_above(
            commands, file_path, EnvExtendType.HARD
        ) as s:
            compiled = s.run()
            env = s.env

        importable = env.var.export_variables(True, wrap=True)
        self.env.var.import_variables(importable)

        return compiled
