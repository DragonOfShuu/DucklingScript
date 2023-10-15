from .base_command import BaseCommand


class Gui(BaseCommand):
    names = ["GUI", "WINDOWS"]

    def verify_arg(self, i: str) -> str | None:
        return (
            None if len(i) == 1 else "Only one character is required. No more or less."
        )
