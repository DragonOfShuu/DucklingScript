from .bases.doc_command import ArgReqType
from ducklingscript.compiler.stack_return import CompiledReturn

from ..environment import Environment
from ..pre_line import PreLine
from .bases import Arguments, Line, SimpleCommand


class DefaultDelay(SimpleCommand):
    names = ["DEFAULT_DELAY", "DEFAULTDELAY"]
    tokenize_args = True
    arg_type = int
    arg_req = ArgReqType.REQUIRED

    sys_var = "$DEFAULT_DELAY"

    @classmethod
    def init_env(cls, env: Environment) -> None:
        env.new_system_var(cls.sys_var, 0)

    def verify_args(self, args: Arguments) -> str | None:
        if len(args) > 1:
            self.stack.add_warning(
                "Setting the default delay multiple times is unnecessary."
            )

    def run_compile(self, commandName: PreLine, arg: Line) -> str | list[str] | CompiledReturn | None:
        self.env.edit_system_var(self.sys_var, arg.content)

        return super().run_compile(commandName, arg)
