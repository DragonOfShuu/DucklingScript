from typing import TYPE_CHECKING

from ducklingscript.compiler.commands.bases.simple_command import ArgLine
from ..tokenization.token_value_types import WrappedType
from ..environments.value_types.wrapped_variable import WrappedVariable
from ..environments.env_extend_type import EnvExtendType
from .utility.file_path import convert_to_path
from ducklingscript.compiler.compiled_ducky import CompiledDucky
from ..errors import NotAValidCommandError
from ducklingscript.compiler.pre_line import PreLine
from .bases.simple_command import SimpleCommand
from ..environments.packaged_variables import PackagedVariables

if TYPE_CHECKING:
    from ..environments.environment import Environment

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

    def _containerize_imported(
        self, module_name: str, packaged: PackagedVariables, current_env: "Environment"
    ) -> PackagedVariables:
        packed_var_dict: dict[str, WrappedType] = {
            **packaged.user_vars,
            **packaged.temp_vars,
            **packaged.system_vars,
        }
        return PackagedVariables(
            user_vars={module_name: WrappedVariable(current_env, packed_var_dict)},
        )

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

        importable = env.var.export_variables(True)
        new_importable = self._containerize_imported(
            file_path.stem, importable, self.env
        )
        self.env.var.import_variables(new_importable)

        return compiled
