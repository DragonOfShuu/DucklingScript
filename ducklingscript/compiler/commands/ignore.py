from ..errors import GeneralError
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from .bases import BlockCommand, ArgReqType

desc = """
Ignore the given block of code. The code given is placed directly
into the output file with no checks.

Please note that this is dangerous, and only recommended if 
you know what you are doing, or need forward compatibility.
"""


class Ignore(BlockCommand):
    names = ["IGNORE"]
    arg_req: ArgReqType = ArgReqType.NOTALLOWED
    description = desc

    def run_compile(
        self,
        commandName: PreLine,
        argument: None,
        code_block: list[PreLine | list],
    ) -> list[str] | CompiledReturn | None:
        raw: list[str] = []
        for i in code_block:
            if isinstance(i, list):
                raise GeneralError(
                    self.stack,
                    "Tabs are not accepted. (Please use triple quotations to use tabs)",
                )
            raw.append(i.content)
        return raw
