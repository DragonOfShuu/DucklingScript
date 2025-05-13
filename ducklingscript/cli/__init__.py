from .compile import compile
from .version import version
from .help import help
from .app import app
from .all import all
from .new import new
from .interpret import interpret

all_commands = [compile, version, help, all, new, interpret]

for command in all_commands:
    app.command()(command)

__all__ = ["app"]
