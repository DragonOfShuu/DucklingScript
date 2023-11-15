from .bases import SimpleCommand, ArgReqType


class Extended(SimpleCommand):
    names = [
        "BREAK",
        "PAUSE",
        "CAPSLOCK",
        "DELETE",
        "END",
        "ESC",
        "ESCAPE",
        "HOME",
        "INSERT",
        "NUMLOCK",
        "PAGEUP",
        "PAGEDOWN",
        "PRINTSCREEN",
        "SCROLLLOCK",
        "SPACE",
        "TAB",
        "FN",
    ]

    arg_req = ArgReqType.NOTALLOWED
