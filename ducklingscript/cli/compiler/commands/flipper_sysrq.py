from .base_command import BaseCommand


class FlipperSysrq(BaseCommand):
    names = ["SYSRQ"]
    flipper_only = True

    @staticmethod
    def verify_arg(i: str) -> str | None:
        return None if len(i.strip()) == 1 else "This command is one char only"

    @staticmethod
    def format_arg(arg: str) -> str:
        return arg.strip()
