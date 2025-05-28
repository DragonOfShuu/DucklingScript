from typer import Typer

from .plugins import app as plugins_app

app_help = """
The CLI for the DucklingScript
programming language.
"""

app = Typer(help=app_help, add_completion=False)
app.add_typer(plugins_app, name="plugins", help="Manage DucklingScript plugins")
