from dataclasses import dataclass, asdict


@dataclass
class CompileOptions:
    stack_limit: int = 20
    """
    The number of allowed stacks
    before it is considered a 
    stack overflow.
    """
    include_comments: bool = False
    """
    If comments should show up
    in the compiled file
    """
    flipper_commands: bool = True
    """
    Allow the use of flipper
    only commands inside the
    compiler.
    """
    quackinter_commands: bool = True
    """
    Allow the use of quackinter
    commands inside the compiler.
    """
    supress_command_not_exist: bool = False
    """
    Supress warnings that state
    that a given command does not
    exist.
    """
    use_project_config: bool = True
    """
    Use the config file found
    inside of the configuration.
    """
    create_sourcemap: bool = False
    """
    Create a sourcemap along with
    the given code that allows
    backtracking and finding
    what code executed.

    ## !!! USE ONLY IF YOU NEED TO WRITE A SOURCEMAP TO A FILE !!!

    ### If you don't need a file, just use `CompiledDucky.get_duckling_stacktrace`
    """

    def to_dict(self):
        """
        Convert these options
        into a dictionary.
        """
        return asdict(self)
