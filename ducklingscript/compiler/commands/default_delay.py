from typing import Any

from ducklingscript.compiler.stack_return import CompiledReturn
from ducklingscript.compiler.tokenization import token_return_types

from ..environment import Environment
from ..pre_line import PreLine
from .bases import SimpleCommand
from ..tokenization import Tokenizer


class DefaultDelay(SimpleCommand):
    names = ["DEFAULT_DELAY", "DEFAULTDELAY"]
    tokenize_args = True
    arg_type = int

    sys_var = "$DEFAULT_DELAY"

    @classmethod
    def init_env(cls, env: Environment) -> None:
        env.new_system_var(cls.sys_var, 0)

    def run_compile(
        self, commandName: PreLine, all_args: list[token_return_types]
    ) -> list[str] | CompiledReturn | None:
        if len(all_args) > 1:
            self.stack.add_warning(
                "Setting the default delay multiple times is unnecessary."
            )

        returnable = []
        for i in all_args:
            returnable.append(f"{commandName.cont_upper()} {i}")
            self.env.edit_system_var(self.sys_var, int(i))

        return returnable
