from .utility.file_path import convert_to_path
from ..environments.env_extend_type import EnvExtendType
from ..compiled_ducky import CompiledDucky
from ..pre_line import PreLine
from ..errors import NotAValidCommandError
from .bases.simple_command import ArgLine, SimpleCommand
from .bases.doc_command import ArgReqType


class From(SimpleCommand):
    """
    Command to import a module or file.
    """

    names = ["FROM"]
    arg_req = ArgReqType.REQUIRED
    arg_type = "<FilePath> IMPORT <Variable|Function>,<Variable|Function>..."
    description = "Imports a module or file into the current environment, while still allowing it to be ran in its own environment."

    def separate_parts(self, content: str):
        parts = content.split(maxsplit=2)
        return parts[0], [i.strip() for i in parts[2].split(",")]

    def verify_arg(self, arg: ArgLine) -> str | None:
        if arg.content.endswith("."):
            return "The dot operator cannot appear alone at the end of path."

    def run_compile(self, command_name: PreLine, arg: ArgLine) -> CompiledDucky | None:
        from ..compiler import DucklingCompiler

        if self.stack.file is None:
            raise NotAValidCommandError(
                self.stack, "The FROM command cannot be used outside of a file."
            )

        raw_file_path, import_vars = self.separate_parts(arg.content)

        file_path = convert_to_path(self.stack_pile, self.stack.file, raw_file_path)

        with file_path.open() as f:
            text = f.read().splitlines()

        file_index = self.env.proj.register_file(file_path)

        commands = DucklingCompiler._prepare_for_stack(text, file_index)

        with self.stack_pile.add_stack_above(
            commands, file_path, EnvExtendType.HARD
        ) as s:
            compiled = s.run()
            env = s.env

        importable = env.var.export_variables(
            (None if "*" in import_vars else import_vars), wrap=True
        )
        self.env.var.import_variables(importable)

        return compiled
