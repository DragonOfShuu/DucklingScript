from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.tokenization import token_return_types
from .bases import SimpleCommand
from ..stack_return import CompiledReturn, StackReturnType
from ..errors import InvalidArguments
from ..tokenization import Tokenizer


class Return(SimpleCommand):
    names = ["RETURN", "RET"]
    can_have_arguments = False
    tokenize_args = True

    def run_compile(
        self, commandName: PreLine, all_args: list[token_return_types]
    ) -> list[str] | CompiledReturn | None:
        if len(all_args)>1:
            raise InvalidArguments(self.stack, "")
        
        argument = None if not all_args else all_args[0]

        return CompiledReturn(return_type=StackReturnType.CONTINUE, return_data=argument)
