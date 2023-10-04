from .base_command import BaseCommand


class ArrowKeys(BaseCommand):
    names = [
        "DOWNARROW", "DOWN",
        "LEFTARROW", "LEFT",
        "RIGHTARROW", "RIGHT",
        "UPARROW", "UP"
    ]

    can_have_arguments = False