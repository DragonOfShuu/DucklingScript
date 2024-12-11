from rich import print
from importlib.metadata import version as importlib_version


def version():
    assert (
        __package__ is not None
    ), "To run this command, it must be ran inside the package!"
    print(
        f"[dark_orange]DucklingScript[/dark_orange] is version {importlib_version('ducklingscript')}"
    )
