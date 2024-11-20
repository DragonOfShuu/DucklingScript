from .bases.simple_command import SimpleCommand


desc = """
Print out text while using the Quackinter
interpreter.
"""


class QuackinterPrintln(SimpleCommand):
    names = ["PRINTLN"]
    quackinter_only = True
    strip_args = False
    description = desc
