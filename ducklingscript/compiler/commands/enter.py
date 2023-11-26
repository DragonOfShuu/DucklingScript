from .bases.doc_command import ArgReqType
from .bases import SimpleCommand

desc = """
As if the user was to press the enter key.
"""


class Enter(SimpleCommand):
    names = ["ENTER"]
    arg_req = ArgReqType.NOTALLOWED
    description = desc
