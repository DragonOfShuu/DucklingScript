from pathlib import Path
from ducklingscript import (
    DuckyScriptError,
    CompileOptions,
)
from .components.compile_component import CompileComponent
from ..compiler.compiler import Compiled
from .utils import Configuration
from typing import Annotated
from rich import print
from rich.progress import Progress, TextColumn, SpinnerColumn
import typer

filename_type = Annotated[
    Path,
    typer.Argument(
        help="The file to be compiled",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
]
output_type = Annotated[
    Path,
    typer.Argument(
        help="The file to compile to",
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=False,
        resolve_path=True,
    ),
]


def compile(
    filename: filename_type,
    output: output_type = Path("a.txt"),
    stack_limit: Annotated[
        int,
        typer.Option(
            help="The max amount of stacks allowed in your program", min=5, max=200
        ),
    ] = Configuration.config.stack_limit,
    comments: Annotated[
        bool, typer.Option(help="If comments should appear in the compiled file")
    ] = Configuration.config.include_comments,
    sourcemap: Annotated[
        bool, typer.Option(help="If we should make a sourcemap")
    ] = Configuration.config.create_sourcemap,
):
    """
    Compile a file, and output it to the given location with the given name.
    """
    options = Configuration.config.to_dict()
    options.update({"stack_limit": stack_limit})
    options.update({"include_comments": comments})
    options.update({"create_sourcemap": sourcemap})
    compile_options = CompileOptions(**options)

    compiled: Compiled | None = None
    error: DuckyScriptError | None = None
    compile_component = CompileComponent.get()
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Compiling...", total=None)
            compiled = compile_component.prepare_and_compile(
                filename, output, compile_options
            )
    except DuckyScriptError as e:
        error = e

    print("---")

    if compiled:
        compile_component.compile_successful(compiled)
    elif error:
        compile_component.compile_with_error(error)
    else:
        print(
            "Unknown error occurred... No actual error, but no compiled code found..."
        )
