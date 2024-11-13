from .bases.doc_command import ArgReqType
from .bases.simple_command import SimpleCommand

desc = """
Wait for a button press before continuing execution.
"""

class FlipperWaitForButtonPress(SimpleCommand):
    names = ["WAITFORBUTTONPRESS", "WAIT_FOR_BUTTON_PRESS"]
    arg_req = ArgReqType.NOTALLOWED
    flipper_only = True
    description = desc
