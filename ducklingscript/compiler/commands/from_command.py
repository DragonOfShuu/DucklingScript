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
    description = "Imports a module or file into the current environment, while still allowing it to be ran in its own environment."

    def separate_parts(self, content: str):
        parts = content.split(maxsplit=2)
        return parts[0], [i.strip() for i in parts[2]]

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

        # collected_variables = {}
        # all_vars = env.var.all_vars
        # for variable in import_vars:
        #     if variable not in all_vars:
        #         raise VarIsNonExistentError(self.stack_pile, f"Variable {variable} is non existent in this file's environment.")
        #     collected_variables[variable] = all_vars[variable]

        # Use Variable Environment built in functions

        importable = env.var.export_variables(import_vars, wrap=True)
        self.env.var.import_variables(importable)

        return compiled

        # run_parallel = command_name.content_as_upper() != "STARTCODE"
        # with self.stack_pile.add_stack_above(commands, file_path, EnvExtendType.PARALLEL if run_parallel else EnvExtendType.NORMAL) as s:
        #     compiled = s.run()

        # if command_name.content_as_upper() in ["START", "STARTCODE"]:
        #     return compiled
        # elif command_name.content_as_upper() == "STARTENV":
        #     return CompiledDucky()
