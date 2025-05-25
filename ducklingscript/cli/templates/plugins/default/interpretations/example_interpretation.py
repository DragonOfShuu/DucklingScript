from ..main import plugin

from quackinter import Command

@plugin.interpretation()
class ExampleInterpretation(Command):
    """
    An example interpretation for the DucklingScript CLI.
    This interpretation does nothing but serves as a template for creating new interpretations.
    """

    # def run(self, *args, **kwargs):
    #     # Remember, for interpretations all we are doing is converting DucklingScript to Ducky
    #     return f"STRINGLN Hello, {args[0].content if args else 'World'}!"