from ducklingscript import SimpleCommand, ArgReqType
from ducklingscript.compiler.commands.bases.simple_command import ArgLine

media_args = [
    # Machine Commands
    "POWER",
    "REBOOT",
    "SLEEP",
    "LOGOFF",
    "VOLUME_UP",
    "VOLUME_DOWN",
    "BRIGHT_UP",
    "BRIGHT_DOWN",
    # Keys
    "HOME",
    "BACK",
    "FORWARD",
    "REFRESH",
    "SNAPSHOT",
    # Media
    "PLAY",
    "PAUSE",
    "PLAY_PAUSE",
    "NEXT_TRACK",
    "PREV_TRACK",
    "STOP",
    "MUTE",
    # Mac
    "FN",
    # Misc
    "EJECT",
    "EXIT",
]

class FlipperMedia(SimpleCommand):
    names = ["MEDIA"]
    arg_req = ArgReqType.REQUIRED
    flipper_only = True

    def format_arg(self, arg: ArgLine) -> ArgLine:
        return arg.update_func(str.upper)

    def verify_arg(self, arg: ArgLine) -> str | None:
        if arg.content.upper() not in media_args:
            return 'Argument given to media is not a proper media argument.'
