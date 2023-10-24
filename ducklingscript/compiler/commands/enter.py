from .bases import SimpleCommand


class Enter(SimpleCommand):
    names = ["ENTER"]
    can_have_arguments = False
