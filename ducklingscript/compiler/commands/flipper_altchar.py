from .bases.doc_command import ArgReqType
from .bases import ArgLine, SimpleCommand

desc = """
As if the user were to type a key
using alt codes.
"""


class FlipperAltChar(SimpleCommand):
    names = ["ALTCHAR"]
    flipper_only = True
    arg_type = str
    arg_req = ArgReqType.REQUIRED

    description = desc

    def verify_arg(self, arg: ArgLine) -> str | None:
        return (
            None
            if arg.content.strip().isdigit() and len(arg.content.strip()) <= 4
            else "Argument must be a number, and 4 digits or less."
        )
