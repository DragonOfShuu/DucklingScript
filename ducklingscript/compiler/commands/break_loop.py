from .bases import SimpleCommand, ArgReqType
from ..stack_return import CompiledReturn, StackReturnType


class BreakLoop(SimpleCommand):
    names = ["BREAK_LOOP", "BREAKLOOP"]
    arg_req = ArgReqType.NOTALLOWED

    def multi_comp(self, commandName, all_args) -> list[str] | CompiledReturn | None:
        return CompiledReturn(return_type=StackReturnType.BREAK)
