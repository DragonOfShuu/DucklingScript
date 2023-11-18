from .bases import Line, SimpleCommand


class FlipperModifierKeys(SimpleCommand):
    names = ["CTRL-ALT", "CTRL-SHIFT", "ALT-SHIFT", "ALT-GUI", "GUI-SHIFT"]
    flipper_only = True

    def verify_arg(self, arg: Line) -> str | None:
        return (
            None
            if len(arg.content) == 1
            else "This command only allows 1 character. No more no less."
        )
