from .bases.doc_command import ArgReqType
from .bases import SimpleCommand


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

    arg_req = ArgReqType.NOTALLOWED
