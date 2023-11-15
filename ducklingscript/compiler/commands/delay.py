from .bases import SimpleCommand, ArgReqType


class Delay(SimpleCommand):
    names = ["DELAY"]
    tokenize_args = True
    arg_type = int
    arg_req = ArgReqType.REQUIRED

    def verify_arg(self, i: int) -> str | None:
        if i < 0:
            return "Delay value cannot be below 0."
