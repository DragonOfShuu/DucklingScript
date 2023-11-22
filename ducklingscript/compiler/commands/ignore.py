from .bases.doc_command import ArgReqType
from ..errors import GeneralError
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from .bases import BlockCommand


class Ignore(BlockCommand):
    arg_req: ArgReqType = ArgReqType.NOTALLOWED

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
