from .bases.doc_command import ArgReqType
from .bases.simple_command import SimpleCommand

desc = """
The extra keys that the flipper adds.
"""


class FlipperExtended(SimpleCommand):
    arg_req = ArgReqType.NOTALLOWED
    names = ["BACKSPACE", "GLOBE", *[f"F{n+1}" for n in range(12)]]
    flipper_only = True
    description = desc
