from ..errors import CompilationError
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.compiled_ducky import CompiledDucky, CompiledDuckyLine
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
        command_name: PreLine,
        argument: None,
        code_block: list[PreLine | list],
    ) -> CompiledDucky | None:
        raw = CompiledDucky()
        for i in code_block:
            if isinstance(i, list):
                raise CompilationError(
                    self.stack,
                    "Tabs are not accepted. (Please use triple quotations to use tabs)",
                )
            raw.add_lines(CompiledDuckyLine(i, i.content))
        return raw
