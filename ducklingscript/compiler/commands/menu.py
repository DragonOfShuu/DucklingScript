from .bases import SimpleCommand


class Menu(SimpleCommand):
    names = ["MENU"]
    can_have_arguments = False
