from .example_command import ExampleCommand as ExampleCommand
from .example_powershell_command import (
    ExamplePowerShellCommand as ExamplePowerShellCommand,
)

all_commands = [ExampleCommand, ExamplePowerShellCommand]

__all__ = ["all_commands"]
