from .compile import compile
from .version import version
from .help import help
from .app import app
from .all import all
from .new import new
from .interpret import interpret
from .plugins import app as plugins_app


app.add_typer(plugins_app, name="plugins", help="Manage DucklingScript plugins")

all_commands = [compile, version, help, all, new, interpret]

for command in all_commands:
    app.command()(command)


__all__ = ["app"]
