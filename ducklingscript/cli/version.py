from rich import print
import pkg_resources


def version():
    print(
        f"[dark_orange]{__package__}[/dark_orange] is version {pkg_resources.get_distribution(__package__).version}"
    )
