from ducklingscript.compiler.stack_return import CompiledReturn

from ..environment import Environment
from ..pre_line import PreLine
from .bases import SimpleCommand, ArgReqType


class DefaultDelay(SimpleCommand):
    names = ["DEFAULT_DELAY", "DEFAULTDELAY"]
    tokenize_args = True
    arg_type = int
    arg_req = ArgReqType.REQUIRED

    sys_var = "$DEFAULT_DELAY"

    @classmethod
    def init_env(cls, env: Environment) -> None:
        env.new_system_var(cls.sys_var, 0)

    def multi_comp(self, commandName, all_args) -> list[str] | CompiledReturn | None:
        if len(all_args) > 1:
            self.stack.add_warning(
                "Setting the default delay multiple times is unnecessary."
            )
        return super().multi_comp(commandName, all_args)

    def run_compile(
        self, commandName: PreLine, arg: int
    ) -> str | list[str] | CompiledReturn | None:
        self.env.edit_system_var(self.sys_var, int(arg))

        return super().run_compile(commandName, arg)
