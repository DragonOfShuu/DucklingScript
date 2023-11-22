from .bases.doc_command import ArgReqType
from .bases import SimpleCommand


class FlipperAltCode(SimpleCommand):
    names = ["ALTCODE"]
    flipper_only = True
    arg_req = ArgReqType.REQUIRED
