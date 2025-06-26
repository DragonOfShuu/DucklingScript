from typing import TYPE_CHECKING

from .bases.doc_command import ArgReqType
from .bases.base_command import BaseCommand

if TYPE_CHECKING:
    from ducklingscript.compiler.stack import Stack

class ImportCommand(BaseCommand):
    """
    Command to import a module or file.
    """

    names = ["IMPORT"]
    arg_req = ArgReqType.REQUIRED
    description = "Imports a module or file into the current environment, while still allowing it to be ran in its own environment."

    def run_compile(self, command_name: str, arg: str) -> str:
        # Here you would implement the logic to import the module or file
        # For now, we just return a placeholder string
        return f"Importing {arg} in {command_name}"
    
    def run_is_this_command(self, command_name: str, argument: str | None, code_block: list[str] | None, stack: Stack | None = None) -> bool:
        ...