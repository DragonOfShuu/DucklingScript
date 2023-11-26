from .bases.doc_command import ArgReqType
from .bases import SimpleCommand

desc = """
As if the user was pressing an arrow key.
"""


class ArrowKeys(SimpleCommand):
    names = [
        "DOWNARROW",
        "DOWN",
        "LEFTARROW",
        "LEFT",
        "RIGHTARROW",
        "RIGHT",
        "UPARROW",
        "UP",
    ]
    description = desc

    arg_req = ArgReqType.NOTALLOWED
