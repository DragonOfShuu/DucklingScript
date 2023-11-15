from .bases import SimpleCommand, ArgReqType


class FlipperAltCode(SimpleCommand):
    names = ["ALTCODE"]
    flipper_only = True
    arg_req = ArgReqType.REQUIRED
