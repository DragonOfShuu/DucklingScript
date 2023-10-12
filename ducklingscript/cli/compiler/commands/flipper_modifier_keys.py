from .base_command import BaseCommand


class FlipperModifierKeys(BaseCommand):
    names = ["CTRL-ALT", "CTRL-SHIFT", "ALT-SHIFT", "ALT-GUI", "GUI-SHIFT"]
    flipper_only = True

    @staticmethod
    def verify_arg(i: str) -> str | None:
        return (
            None
            if len(i) == 1
            else "This command only allows 1 character. No more no less."
        )