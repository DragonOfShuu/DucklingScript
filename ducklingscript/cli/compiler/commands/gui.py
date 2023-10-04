from .base_command import BaseCommand


class Gui(BaseCommand):
    names = ["GUI", "WINDOWS"]

    @staticmethod
    def verify_arg(i: str) -> str | None:
        return (
            None if len(i) == 1 else "Only one character is required. No more or less."
        )
