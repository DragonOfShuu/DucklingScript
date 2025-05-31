from __future__ import annotations
from typing import overload

from rich import print

from .cli_component import CliComponent


class GeneralComponent(CliComponent):
    @classmethod
    def get(cls) -> GeneralComponent:
        if cls._component:
            return cls._component
        new_component = cls()
        cls._component = new_component
        return new_component

    def print(self, message: str):
        print(message)

    @overload
    def print_error(self, error: str): ...
    @overload
    def print_error(self, error: Exception): ...
    def print_error(self, error: Exception|str):
        if isinstance(error, Exception):
            print(f"[red]{error.__class__.__name__}[/red]: {error}")
        else:
            print(f"[red]Error:[/red] {error}")
    
    def print_warning(self, warning: str):
        print(f"[yellow]Warning:[/yellow] {warning}")