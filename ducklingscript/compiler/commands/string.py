from .bases import SimpleCommand


class String(SimpleCommand):
    names = ["STRING", "STRINGLN"]
    strip_args = False
