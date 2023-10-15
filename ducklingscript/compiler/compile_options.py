from dataclasses import dataclass, asdict


@dataclass
class CompileOptions:
    stack_limit: int = 20
    include_comments: bool = False

    def to_dict(self):
        return asdict(self)
