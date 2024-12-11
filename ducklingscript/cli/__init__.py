from .compile import compile
from .version import version
from .help import help
from .app import app
from .all import all
from .new import new
from .interpret import interpret

all_commands = [compile, version, help, all, new]

app.command()(compile)
app.command()(version)
app.command()(help)
app.command()(all)
app.command()(new)
app.command()(interpret)

__all__ = ["app"]
