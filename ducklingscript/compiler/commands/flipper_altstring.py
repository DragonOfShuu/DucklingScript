from .bases import SimpleCommand, ArgReqType


class FlipperAltString(SimpleCommand):
    names = ["ALTSTRING"]
    flipper_only = True
    arg_req = ArgReqType.REQUIRED
