# from ducklingscript.cli.compiler.pre_line import PreLine
from ..pre_line import PreLine
from dataclasses import dataclass, asdict

from .bases.base_command import BaseCommand
from .bases.block_command import BlockCommand
from .bases.simple_command import SimpleCommand

from .alt import Alt
from .arrow_keys import ArrowKeys
from .ctrl import Ctrl
from .break_loop import BreakLoop
from .continue_loop import ContinueLoop
from .default_delay import DefaultDelay
from .delay import Delay
from .extended import Extended
from .enter import Enter
from .func import Func
from .gui import Gui
from .if_command import If
from .menu import Menu
from .not_exists import NotExists
from .print_command import Print
from .rem import Rem
from .repeat import Repeat
from .ret import Return
from .run import Run
from .shift import Shift
from .start import Start
from .string import String
from .var import Var
from .while_loop import While
from .whitespace import Whitespace

from .flipper_altchar import FlipperAltChar
from .flipper_altcode import FlipperAltCode
from .flipper_altstring import FlipperAltString
from .flipper_modifier_keys import FlipperModifierKeys
from .flipper_sysrq import FlipperSysrq

command_palette: list[type[BaseCommand]] = [
    Alt,
    ArrowKeys,
    BreakLoop,
    ContinueLoop,
    Ctrl,
    DefaultDelay,
    Delay,
    Enter,
    Extended,
    Func,
    Gui,
    If,
    Menu,
    NotExists,
    Print,
    Rem,
    Repeat,
    Return,
    Run,
    Shift,
    String,
    Start,
    Var,
    While,
    Whitespace,
    FlipperAltChar,
    FlipperAltCode,
    FlipperAltString,
    FlipperModifierKeys,
    FlipperSysrq,
]


@dataclass
class ParsedCommand:
    commandName: PreLine
    argument: str | None = None
    code_block: list[PreLine] | None = None

    def asdict(self):
        return asdict(self)
