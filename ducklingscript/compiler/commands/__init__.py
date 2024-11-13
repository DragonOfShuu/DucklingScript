from .bases import BaseCommand, BlockCommand, SimpleCommand, DocCommand

from .bases import ArgReqType, Arguments, ArgLine

from .alt import Alt
from .arrow_keys import ArrowKeys
from .ctrl import Ctrl
from .break_loop import BreakLoop
from .continue_loop import ContinueLoop
from .default_delay import DefaultDelay
from .delay import Delay
from .enter import Enter
from .exist import Exist
from .extended import Extended
from .func import Func
from .gui import Gui
from .if_command import If
from .ignore import Ignore
from .menu import Menu
from .not_exist import NotExist
from .pass_command import Pass
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
from .flipper_default_string_delay import FlipperDefaultStringDelay
from .flipper_extended import FlipperExtended
from .flipper_hold_release import FlipperHoldRelease
from .flipper_media import FlipperMedia
from .flipper_modifier_keys import FlipperModifierKeys
from .flipper_sysrq import FlipperSysrq
from .flipper_wait_for_button_press import FlipperWaitForButtonPress

from .quackinter_general_keys import QuackinterGeneralKey

command_palette: list[type[BaseCommand]] = [
    Alt,
    ArrowKeys,
    BreakLoop,
    ContinueLoop,
    Ctrl,
    DefaultDelay,
    Delay,
    Enter,
    Exist,
    Extended,
    Func,
    Gui,
    If,
    Ignore,
    Menu,
    NotExist,
    Pass,
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
    FlipperDefaultStringDelay,
    FlipperExtended,
    FlipperHoldRelease,
    FlipperMedia,
    FlipperModifierKeys,
    FlipperSysrq,
    FlipperWaitForButtonPress,

    QuackinterGeneralKey,
]
