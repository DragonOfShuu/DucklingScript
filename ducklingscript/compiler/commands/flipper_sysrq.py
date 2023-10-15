from .base_command import BaseCommand


class FlipperSysrq(BaseCommand):
    names = ["SYSRQ"]
    flipper_only = True

    def verify_arg(self, i: str) -> str | None:
        return None if len(i.strip()) == 1 else "This command is one char only"

    def format_arg(self, arg: str) -> str:
        return arg.strip()
