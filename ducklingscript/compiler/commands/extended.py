from .bases.doc_command import ArgReqType
from .bases import SimpleCommand

desc = """
As if the user was to press one of the given keys.
"""


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
