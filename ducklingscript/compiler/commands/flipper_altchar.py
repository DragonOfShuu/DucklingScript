from .bases import SimpleCommand, ArgReqType


class FlipperAltChar(SimpleCommand):
    names = ["ALTCHAR"]
    flipper_only = True
    arg_type = str
    arg_req = ArgReqType.REQUIRED

    def verify_arg(self, i: str) -> str | None:
        return (
            None
            if i.strip().isdigit() and len(i.strip()) <= 4
            else "Argument must be a number, and 4 digits or less."
        )
