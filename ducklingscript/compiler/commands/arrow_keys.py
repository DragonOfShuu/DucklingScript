from .bases import SimpleCommand, ArgReqType


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
