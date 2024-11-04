from .bases.doc_command import ArgReqType
from .bases import ArgLine, SimpleCommand

desc = """
Wait before executing the subsequent command. Give the delay in milliseconds.
"""


class Delay(SimpleCommand):
    names = ["DELAY"]
    tokenize_args = True
    arg_type = int
    arg_req = ArgReqType.REQUIRED
    description = desc

    def verify_arg(self, arg: ArgLine) -> str | None:
        if arg.content < 0:
            return "Delay value cannot be below 0."
