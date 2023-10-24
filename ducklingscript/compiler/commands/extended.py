from .bases import SimpleCommand


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

    can_have_arguments = False
