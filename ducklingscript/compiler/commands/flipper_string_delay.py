from .bases.doc_command import ArgReqType
from .bases.simple_command import Arguments, SimpleCommand


class FlipperStringDelay(SimpleCommand):
    """
    Change the delay between key presses
    for the line of code directly beneath
    this one.
    """
    names = ["STRINGDELAY", "STRING_DELAY"]
    flipper_only = True
    tokenize_args = True
    arg_req = ArgReqType.REQUIRED
    arg_type = int

    def verify_args(self, args: Arguments) -> str | None:
        if len(args) > 1:
            self.stack.add_warning(
                "Setting the default delay multiple times is unnecessary."
            )
