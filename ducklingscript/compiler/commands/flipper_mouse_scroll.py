from .bases.doc_command import ArgReqType
from .bases.simple_command import SimpleCommand

desc = """
Scroll the mouse by the distance
"""

class FlipperMouseScroll(SimpleCommand):
    names = ["MOUSESCROLL", "MOUSE_SCROLL"]
    description = desc
    flipper_only = True
    arg_req = ArgReqType.REQUIRED
    arg_type = int