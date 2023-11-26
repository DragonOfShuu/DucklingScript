from .bases.doc_command import ArgReqType
from .bases import SimpleCommand

desc = """
As if the user were to type a line of text
using alt codes.
"""


class FlipperAltString(SimpleCommand):
    names = ["ALTSTRING"]
    flipper_only = True
    arg_req = ArgReqType.REQUIRED
    description = desc
