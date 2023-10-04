from pathlib import Path
from rich.progress import Progress, SpinnerColumn, TextColumn
from ducklingscript import Compiler, CompilationError, StackableError
from typing import Annotated
from rich import print
import pkg_resources
import typer

app = typer.Typer()

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


@app.command()
def compile(filename: filename_type, output: output_type = Path("a.txt")):
    try:
        __prepare_and_compile(filename, output)
    except CompilationError as e:
        if isinstance(e, StackableError):
            all_error = "\n".join(e.stack_traceback(5))
            print(f"[red]{all_error}[/red]")
        print(f"[bold red]{type(e).__name__}:[/bold red] {e.args[0]}")
    else:
        print(f"[bold green]Compilation complete![/bold green]")


def __prepare_and_compile(filename: Path, output: Path):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Compiling...", total=None)
        compiled = Compiler().compile_file(filename)
        for warning in compiled[1].retrieve_warnings():
            warning_str = "\n".join(warning)
            print(f"[orange3]{warning_str}[/orange3]")

        output.write_text("\n".join(compiled[0]))


@app.command()
def version():
    print(
        f"[dark_orange]{__package__}[/dark_orange] is version {pkg_resources.get_distribution(__package__).version}"
    )


if __name__ == "__main__":
    app()
