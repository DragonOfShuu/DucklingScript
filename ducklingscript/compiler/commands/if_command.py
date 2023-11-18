from ducklingscript.compiler.environment import Null
from ..errors import InvalidArguments
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from .bases import BlockCommand


IF_SUCCESS = "$IF_SUCCESS"


class If(BlockCommand):
    names = ["IF", "ELIF", "ELSE"]
    argument_required = False

    def mk_temp_var(self):
        value = self.env.temp_vars.get(IF_SUCCESS, Null())
        if isinstance(value, Null):
            self.env.new_temp_var(IF_SUCCESS, False)

    def run_compile(
        self,
        commandName: PreLine,
        argument: str | None,
        code_block: list[PreLine | list],
    ) -> list[str] | CompiledReturn | None:
        name = commandName.cont_upper()
        self.mk_temp_var()

        # If and Elif must have args
        if argument is None and name != "ELSE":
            raise InvalidArguments(self.stack, "IF and ELIF must have an argument.")

        # ELSE must not have args
        if argument is not None and name == "ELSE":
            raise InvalidArguments(self.stack, "ELSE cannot have an argument.")

        tokenized = None
        if name != "ELSE":
            tokenized = self.token_arg

        # If this is an if statement,
        # we disregard previous statements
        if name == "IF":
            self.env.edit_temp_var(IF_SUCCESS, False)
        elif self.env.temp_vars.get(IF_SUCCESS):
            return

        # Check if statement is true
        if name != "ELSE" and not tokenized:
            return

        # If true, set to disregard
        # future statements
        self.env.edit_temp_var(IF_SUCCESS, True)
        with self.stack.add_stack_above(code_block) as st:
            x = st.run()
        return x
