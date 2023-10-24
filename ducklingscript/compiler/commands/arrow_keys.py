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

    can_have_arguments = False
