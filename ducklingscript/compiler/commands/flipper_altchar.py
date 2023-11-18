from .bases import Line, SimpleCommand, ArgReqType


class FlipperAltChar(SimpleCommand):
    names = ["ALTCHAR"]
    flipper_only = True
    arg_type = str
    arg_req = ArgReqType.REQUIRED

    def verify_arg(self, arg: Line) -> str | None:
        return (
            None
            if arg.content.strip().isdigit() and len(arg.content.strip()) <= 4
            else "Argument must be a number, and 4 digits or less."
        )
