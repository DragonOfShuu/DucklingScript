from .compile import compile
from .version import version
from .help import help
from .app import app

all_commands = [compile, version]

app.command()(compile)
app.command()(version)
app.command()(help)

__all__ = ["app"]
