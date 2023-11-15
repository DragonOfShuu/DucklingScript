from .bases import SimpleCommand, ArgReqType


class Menu(SimpleCommand):
    names = ["MENU"]
    arg_req = ArgReqType.NOTALLOWED
