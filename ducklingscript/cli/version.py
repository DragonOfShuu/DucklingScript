from rich import print
import pkg_resources


def version():
    assert (
        __package__ is not None
    ), "To run this command, it must be ran inside the package!"
    package_name = __package__.split(".")[0]
    print(
        f"[dark_orange]DucklingScript[/dark_orange] is version {pkg_resources.get_distribution(package_name).version}"
    )
