from .bases.doc_command import ArgReqType
from .bases import SimpleCommand


class FlipperAltString(SimpleCommand):
    names = ["ALTSTRING"]
    flipper_only = True
    arg_req = ArgReqType.REQUIRED
