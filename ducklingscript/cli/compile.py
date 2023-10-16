from pathlib import Path
from rich.progress import Progress, SpinnerColumn, TextColumn
from ducklingscript import Compiler, CompilationError, StackableError, CompileOptions, WarningsObject
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
        compiled = __prepare_and_compile(filename, output, compile_options)
    except CompilationError as e:
        print("---")
        if isinstance(e, StackableError):
            all_error = "\n".join(e.stack_traceback(5))
            print(f"[red]{all_error}[/red]")
        print(f"[bold red]{type(e).__name__}:[/bold red] {e.args[0]}")
        print(f"---\n[bold bright_red]Compile failed with an error.[/bold bright_red] ⛔\n---")
    else:
        print("---")
        print(f"[bold green]Compilation complete![/bold green] ✨")
        if warn:=compiled.warnings:
            print(f"[orange3](with {len(warn)} warning{'s' if len(warn)>1 else ''})[/orange3]")
        print("---")


def display_warnings(warnings: WarningsObject):
    title_col = "bold yellow1"
    text_col = "orange3"
    for warning in warnings:
        print("---")
        if warning.stacktrace:
            stack_trace = '\n'.join(warning.stacktrace)
            print(f"[{title_col}] -> Stacktrace[/{title_col}]")
            print(f"[{text_col}]{stack_trace}[/{text_col}]")
        print(f"[{title_col}] -> Warning[/{title_col}]")
        print(f"[{text_col}]{warning.error}[/{text_col}]")

def __prepare_and_compile(
    filename: Path, output: Path, compile_options: CompileOptions
):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Compiling...", total=None)
        compiled = Compiler(compile_options).compile_file(filename)
        display_warnings(compiled.warnings)

        output.write_text("\n".join(compiled.output))
        return compiled
