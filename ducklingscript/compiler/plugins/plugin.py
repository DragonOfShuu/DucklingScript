from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..commands import BaseCommand
    from quackinter import Command as QuackinterCommand


class Plugin:
    def __init__(self, display_name: str, description: str, version: str = "0.1.0"):
        self.display_name = display_name
        self.description = description
        self.version = version
        self.commands: list[type["BaseCommand"]] = []
        self.interpretations: list[type["QuackinterCommand"]] = []

        self._name: str | None = None

    def command(self):
        """
        Decorator to add a command to the plugin.
        This is a convenience method that allows you to
        use the `@plugin.command` decorator to add commands
        to the plugin.
        """

        def wrapper(command: type["BaseCommand"]):
            self.add_command(command)
            return command

        return wrapper

    def interpretation(self):
        """
        Decorator to add an interpretation to the plugin.
        This is a convenience method that allows you to
        use the `@plugin.interpretation` decorator to add
        interpretations to the plugin.
        """

        def wrapper(interpretation: type["QuackinterCommand"]):
            self.add_interpretation(interpretation)
            return interpretation

        return wrapper

    # This is separated from commands in the event
    # that we may want to add more attributes to the
    # command later.
    def add_command(self, command: type["BaseCommand"]):
        self.commands.append(command)

    def add_commands(self, *commands: type["BaseCommand"]):
        self.commands.extend(commands)

    def add_interpretation(self, interpretation: type["QuackinterCommand"]):
        self.interpretations.append(interpretation)

    def add_interpretations(self, *interpretations: type["QuackinterCommand"]):
        self.interpretations.extend(interpretations)

    def get_commands(self):
        return self.commands

    def get_interpretations(self):
        return self.interpretations

    def __repr__(self):
        return f'Plugin(name="{self.display_name}", description="{self.description}")'

    def __str__(self):
        return f"Plugin: {self.display_name}\nDescription: {self.description}"
