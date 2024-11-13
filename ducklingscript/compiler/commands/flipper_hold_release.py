from ducklingscript import SimpleCommand, ArgReqType, ArgLine, CompiledDucky, Environment, PreLine, NoKeyToReleaseError

held_var_sys_key = "$HELD_KEY"

desc = f"""
Hold/Release a key. The mostly recently held key is stored in {held_var_sys_key},
and cleared when released.
"""

class FlipperHoldRelease(SimpleCommand):
    names = ["HOLD", "RELEASE"]
    arg_req = ArgReqType.REQUIRED
    strip_args = True
    description = desc
    flipper_only = True

    HELD_VAR_SYS_KEY = held_var_sys_key
    ALL_HELD_KEYS = "$ALL_HELD_KEYS_DO_NOT_USE"
    '''
    A list of all currently held down keys. 
    
    USE AT YOUR OWN RISK, the DucklingScript 
    tokenizer does not handle lists.
    '''
    
    @classmethod
    def init_env(cls, env: Environment) -> None:
        env.var.new_system_var(cls.HELD_VAR_SYS_KEY, '')
        env.var.new_system_var(cls.ALL_HELD_KEYS, [])

    def verify_arg(self, arg: ArgLine) -> str | None:
        try:
            from quackinter import KeyInjector
        except ImportError:
            return None
        
        # If we have Quackinter installed, we can 
        # check if the arg given is an acceptable key
        if (arg not in KeyInjector.ACCEPTED_KEYS):
            self.stack.add_warning(
                "Key to hold/release is not accepted in Quackinter or known for the flipper"
            )

    def run_compile(self, command_name: PreLine, arg: ArgLine) -> str | list[str] | None | CompiledDucky:
        all_held_keys: list[str] = self.env.var.system_vars[self.ALL_HELD_KEYS]

        if command_name.cont_upper() == "HOLD":
            all_held_keys.append(arg.content)

            if len(all_held_keys):
                self.stack.add_warning(f"The flipper can only hold 5 keys at once, however we are now holding {len(all_held_keys)} keys.")

            self.env.var.edit_system_var(self.HELD_VAR_SYS_KEY, arg.content)
        else:
            if arg.content not in all_held_keys:
                raise NoKeyToReleaseError(self.stack)
            
            all_held_keys.reverse()
            all_held_keys.remove(arg.content)
            all_held_keys.reverse()
            self.env.var.edit_system_var(self.HELD_VAR_SYS_KEY, '')

        return super().run_compile(command_name, arg)
    