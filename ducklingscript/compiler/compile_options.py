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

    def to_dict(self):
        """
        Convert these options
        into a dictionary.
        """
        return asdict(self)
