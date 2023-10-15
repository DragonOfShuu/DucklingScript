from pathlib import Path
from rich.progress import Progress, SpinnerColumn, TextColumn
from ducklingscript import Compiler, CompilationError, StackableError, CompileOptions
from typing import Annotated
from rich import print
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
        help="The file to be compiled",
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
    ] = 20,
    comments: Annotated[
        bool, typer.Option(help="If comments should appear in the compiled file")
    ] = False,
):
    compile_options = CompileOptions(stack_limit, comments)
    try:
        __prepare_and_compile(filename, output, compile_options)
    except CompilationError as e:
        if isinstance(e, StackableError):
            all_error = "\n".join(e.stack_traceback(5))
            print(f"[red]{all_error}[/red]")
        print(f"[bold red]{type(e).__name__}:[/bold red] {e.args[0]}")
    else:
        print(f"---\n[bold green]Compilation complete![/bold green] ✨\n---")


def __prepare_and_compile(
    filename: Path, output: Path, compile_options: CompileOptions
):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Compiling...", total=None)
        compiled = Compiler().compile_file(filename, compile_options)
        for warning in compiled[1].retrieve_warnings():
            warning_str = "\n".join(warning)
            print(f"[orange3]{warning_str}[/orange3]")

        output.write_text("\n".join(compiled[0]))
