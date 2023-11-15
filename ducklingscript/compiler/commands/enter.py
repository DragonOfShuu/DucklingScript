from .bases import SimpleCommand, ArgReqType


class Enter(SimpleCommand):
    names = ["ENTER"]
    arg_req = ArgReqType.NOTALLOWED
