from .bases import Line, SimpleCommand, ArgReqType


class Delay(SimpleCommand):
    names = ["DELAY"]
    tokenize_args = True
    arg_type = int
    arg_req = ArgReqType.REQUIRED

    def verify_arg(self, arg: Line) -> str | None:
        if arg.content < 0:
            return "Delay value cannot be below 0."
