from ducklingscript import PreLine, Environment, ArgReqType, Arguments, SimpleCommand, CompiledDucky, ArgLine

desc = """
Use to define the delay between each character. Give the value in milliseconds
[default value is 80]
"""

class FlipperDefaultStringDelay(SimpleCommand):
    names = ["DEFAULT_STRING_DELAY", "DEFAULTSTRINGDELAY"]
    tokenize_args = True
    arg_type = int
    arg_req = ArgReqType.REQUIRED
    flipper_only = True

    sys_var = "$DEFAULT_STRING_DELAY"
    description = desc

    @classmethod
    def init_env(cls, env: Environment) -> None:
        env.var.new_system_var(cls.sys_var, 0)

    def verify_args(self, args: Arguments) -> str | None:
        if len(args) > 1:
            self.stack.add_warning(
                "Setting the default delay multiple times is unnecessary."
            )

    def run_compile(
        self, command_name: PreLine, arg: ArgLine
    ) -> str | list[str] | CompiledDucky | None:
        self.env.var.edit_system_var(self.sys_var, arg.content)

        return super().run_compile(command_name, arg)
