from ducklingscript import SimpleCommand, ArgReqType
from ..main import plugin

@plugin.command()
class ExamplePowerShellCommand(SimpleCommand):
    """
    An example PowerShell command for the DucklingScript CLI.
    This command does nothing but serves as a template for creating new commands.
    """

    names = ["POWERSHELL"]
    arg_req = ArgReqType.NOTALLOWED
    description = "An example PowerShell command that does nothing."

    def run_compile(self, command_name: str, arg: str | None = None) -> str:
        # This command tells DucklingScript this command exists, and lets the name pass through.
        # This allows Quackinter to then read the command as an interpretation.
        return "POWERSHELL"
