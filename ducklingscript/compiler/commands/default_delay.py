from typing import Any

from ..environment import Environment
from ..pre_line import PreLine
from .base_command import BaseCommand
from ..tokenization import Tokenizer


class DefaultDelay(BaseCommand):
    names = ["DEFAULT_DELAY", "DEFAULTDELAY"]

    sys_var = "default_value"

    @classmethod
    def init_env(cls, env: Environment) -> None:
        env.new_system_var(cls.sys_var, 0)

    def verify_arg(self, i: str) -> str | None:
        new_i = Tokenizer.tokenize(i, self.stack, self.env)
        if not isinstance(new_i, int):
            return "Argument must be of type integer"

    def format_arg(self, arg: str) -> str:
        return str(Tokenizer.tokenize(arg))

    def run_compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine] | None,
        all_args: list[str],
    ) -> list[str] | None:
        if len(all_args) > 1:
            self.stack.add_warning(
                "Setting the default delay multiple times is unnecessary."
            )

        returnable = []
        for i in all_args:
            returnable.append(f"{commandName.cont_upper()} {i}")
            self.env.edit_system_var(self.sys_var, int(i))

        return returnable
