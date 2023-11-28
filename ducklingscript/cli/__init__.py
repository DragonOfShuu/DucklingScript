from .compile import compile
from .version import version
from .help import help
from .app import app
from .all import all

all_commands = [compile, version]

app.command()(compile)
app.command()(version)
app.command()(help)
app.command()(all)

__all__ = ["app"]
