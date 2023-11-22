from .bases.doc_command import ArgReqType
from .bases import SimpleCommand


class Enter(SimpleCommand):
    names = ["ENTER"]
    arg_req = ArgReqType.NOTALLOWED
