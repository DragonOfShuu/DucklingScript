from ..commands import BaseCommand
from quackinter import Command as QuackinterCommand


class Plugin:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.commands: list[type[BaseCommand]] = []
        self.interpretations: list[QuackinterCommand] = []

    # This is separated from commands in the event
    # that we may want to add more attributes to the
    # command later.
    def add_command(self, command: type[BaseCommand]):
        self.commands.append(command)
    
    def add_commands(self, *commands: type[BaseCommand]):
        self.commands.extend(commands)

    def add_interpretation(self, interpretation: QuackinterCommand):
        self.interpretations.append(interpretation)

    def add_interpretations(self, *interpretations: QuackinterCommand):
        self.interpretations.extend(interpretations)

    def get_commands(self):
        return self.commands

    def get_interpretations(self):
        return self.interpretations
    
    def __repr__(self):
        return f"Plugin(name={self.name}, description={self.description})"
    
    def __str__(self):  
        return f"Plugin: {self.name}\nDescription: {self.description}"
