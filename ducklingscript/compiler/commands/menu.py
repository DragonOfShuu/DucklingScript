from .bases.doc_command import ArgReqType
from .bases import SimpleCommand

desc = """
As if the user was to press the context menu key; similar to a right click.
"""


class Menu(SimpleCommand):
    names = ["MENU"]
    arg_req = ArgReqType.NOTALLOWED
    description = desc
