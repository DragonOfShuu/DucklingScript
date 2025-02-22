from .bases.simple_command import SimpleCommand
from .bases.doc_command import ArgReqType

desc = """
Click down on the mouse.
"""


class FlipperMouseClick(SimpleCommand):
    names = ["LEFTCLICK", "LEFT_CLICK", "RIGHTCLICK", "RIGHT_CLICK"]
    description = desc
    arg_req = ArgReqType.NOTALLOWED
    flipper_only = True
