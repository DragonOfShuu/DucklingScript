from .compile import compile
from .version import version
from .app import app

all_commands = [compile, version]

app.command()(compile)
app.command()(version)

__all__ = ["app"]
