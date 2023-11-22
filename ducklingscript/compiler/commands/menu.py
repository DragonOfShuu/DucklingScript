from .bases.doc_command import ArgReqType
from .bases import SimpleCommand


class Menu(SimpleCommand):
    names = ["MENU"]
    arg_req = ArgReqType.NOTALLOWED
