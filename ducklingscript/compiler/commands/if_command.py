from .bases.doc_command import ArgReqType
from ducklingscript.compiler.environments.variable_environment import Null
from ..errors import InvalidArgumentsError
from ducklingscript.compiler.pre_line import PreLine
from ducklingscript.compiler.stack_return import CompiledReturn
from .bases import BlockCommand, Example


IF_SUCCESS = "$IF_SUCCESS"
desc = """
Run the given block of code only if the condition given is true. 
You can chain if statements using ELIF, as well as ELSE. ELSE
only runs if no previous IF/ELIF succeeded.

ALL NAMES DO NOT DO THE SAME THING.
"""

duckling_ex = [
    """
VAR a 10

REM if a is equal to 10
IF a == 10
    REM this code is ran
    STRINGLN Hello World

REM if a is not equal to 10
ELSE 
    STRINGLN Hello World Not Found :/
""",
    """
VAR a 10

IF a > 10
    STRING a is greater than 10
ELIF a < 10
    STRING a is less than 10
ELSE
    STRING a is 10
""",
]

compiled_ex = ["STRINGLN Hello World", "STRING a is 10"]

example_list = [
    Example(duckling=duckling_ex[0], compiled=compiled_ex[0]),
    Example(duckling=duckling_ex[1], compiled=compiled_ex[1]),
]


class If(BlockCommand):
    names = ["IF", "ELIF", "ELSE"]
    arg_req = ArgReqType.ALLOWED
    arg_type = "<boolean>"
    description = desc

    examples = example_list

    def mk_temp_var(self):
        value = self.env.var.temp_vars.get(IF_SUCCESS, Null())
        if isinstance(value, Null):
            self.env.var.new_temp_var(IF_SUCCESS, False)

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
            raise InvalidArgumentsError(
                self.stack, "IF and ELIF must have an argument."
            )

        # ELSE must not have args
        if argument is not None and name == "ELSE":
            raise InvalidArgumentsError(self.stack, "ELSE cannot have an argument.")

        tokenized = None
        if name != "ELSE":
            tokenized = self.token_arg

        # If this is an if statement,
        # we disregard previous statements
        if name == "IF":
            self.env.var.edit_temp_var(IF_SUCCESS, False)
        elif self.env.var.temp_vars.get(IF_SUCCESS):
            return

        # Check if statement is true
        if name != "ELSE" and not tokenized:
            return

        # If true, set to disregard
        # future statements
        self.env.var.edit_temp_var(IF_SUCCESS, True)
        with self.stack.add_stack_above(code_block) as st:
            x = st.run()
        return x
