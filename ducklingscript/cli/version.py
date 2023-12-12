from rich import print
import pkg_resources


def version():
    package_name = __package__.split(".")[0]
    print(
        f"[dark_orange]DucklingScript[/dark_orange] is version {pkg_resources.get_distribution(package_name).version}"
    )
