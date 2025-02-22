from .extended import Extended
from .arrow_keys import ArrowKeys
from .bases.doc_command import ArgReqType
from .bases.simple_command import SimpleCommand

desc = """
The extra keys that the flipper adds.
"""


class FlipperSpecialKeys(SimpleCommand):
    arg_req = ArgReqType.NOTALLOWED
    names = ["BACKSPACE", *[f"F{n+1}" for n in range(12)]] + Extended.names + ArrowKeys.names
    flipper_only = True
    description = desc
