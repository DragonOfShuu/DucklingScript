
from pathlib import Path
from typing import Annotated

import typer


def new_plugin(path: Annotated[Path, typer.Argument(help="Path to the new plugin directory")]):
    path.mkdir(parents=True, exist_ok=True)
    # (path / "__init__.py").write_text()

