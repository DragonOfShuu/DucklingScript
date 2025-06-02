from ..main import plugin

from ducklingscript import SimpleCommand, PreLine, ArgLine, CompiledDucky


@plugin.command()
class ExampleCommand(SimpleCommand):
    """
    An example command for the DucklingScript CLI.
    This command does nothing but serves as a template for creating new commands.
    """

    names = ["EXAMPLE", "EX"]
    description = "An example command that does nothing."

    def run_compile(
        self, command_name: PreLine, arg: ArgLine | None
    ) -> str | list[str] | None | CompiledDucky:
        # Remember, for commands all we are doing is converting DucklingScript to Ducky
        return f"STRINGLN Hello, {arg.content if arg else 'World'}!"
