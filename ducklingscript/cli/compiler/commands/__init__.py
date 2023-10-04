from ducklingscript.cli.compiler.pre_line import PreLine
from dataclasses import dataclass, asdict

from .alt import Alt
from .arrow_keys import ArrowKeys
from .base_command import BaseCommand
from .default_delay import DefaultDelay
from .delay import Delay
from .extended import Extended
from .enter import Enter
from .gui import Gui
from .menu import Menu
from .rem import Rem
from .repeat import Repeat
from .shift import Shift
from .string import String

command_palette: list[type[BaseCommand]] = [
    Alt,
    ArrowKeys,
    DefaultDelay,
    Delay,
    Enter,
    Extended,
    Gui,
    Menu,
    Rem,
    Repeat,
    Shift,
    String,
]


@dataclass
class ParsedCommand:
    commandName: PreLine
    argument: str | None = None
    code_block: list[PreLine] | None = None

    def asdict(self):
        return asdict(self)
