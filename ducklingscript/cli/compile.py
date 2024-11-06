import json
from pathlib import Path
from rich.progress import Progress, SpinnerColumn, TextColumn
from ducklingscript import (
    Compiler,
    CompilationError,
    GeneralError,
    CompileOptions,
    WarningsObject,
)
from ..compiler.errors import StackTraceNode
from ..compiler.stack_return import StdOutData
from ..compiler.compiler import Compiled
from .utils import Configuration
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
    create_sourcemap: Annotated[
        bool, typer.Option(help="If we should make a sourcemap")
    ] = Configuration.config.create_sourcemap
):
    """
    Compile a file, and output it to the given location with the given name.
    """
    options = Configuration.config.to_dict()
    options.update({"stack_limit": stack_limit})
    options.update({"include_comments": comments})
    options.update({"create_sourcemap": create_sourcemap})
    compile_options = CompileOptions(**options)

    compiled: Compiled | None = None
    error: CompilationError | None = None
    try:
        compiled = __prepare_and_compile(filename, output, compile_options)
    except CompilationError as e:
        error = e

    print("---")

    if compiled:
        compile_successful(compiled)
    elif error:
        compile_with_error(error)
    else:
        print(
            "Unknown error occurred... No actual error, but no compiled code found..."
        )


def compile_with_error(e: CompilationError):
    if isinstance(e, GeneralError):
        all_error = "\n".join(listify_stack_nodes(e.stack_traceback(5)))
        print(f"[red]{all_error}[/red]")
    print(f"[bold red]{type(e).__name__}:[/bold red] {e.args[0]}")
    print("---\n[bold bright_red]Compile failed with an error.[/bold bright_red] ⛔")
    print_std_out(e)
    print("---")


def compile_successful(compiled: Compiled):
    print("[bold green]Compilation complete![/bold green] ✨")
    if warn := compiled.warnings:
        print(
            f"[orange3](with {len(warn)} warning{'s' if len(warn)>1 else ''})[/orange3]"
        )
    print_std_out(compiled)
    print("---")


def print_std_out(obj: Compiled | CompilationError):
    if not isinstance(obj, (Compiled, GeneralError)):
        return

    data: list[StdOutData] = []
    if isinstance(obj, Compiled):
        data = obj.std_out
    else:
        if obj.stack is None:
            return
        data = obj.stack.std_out

    if not data:
        return
    print("--> Captured STD:OUT")
    print_std_data(data)


def print_std_data(data: list[StdOutData]):
    file_digit_lengths = {}
    for i in data:
        if i.file is not None and file_digit_lengths.get(i.file) is None:
            file_length = len(i.file.open().readlines())
            digit_length = len(str(file_length))
            file_digit_lengths.update({i.file: digit_length})

        file_str = "" if i.file is None else f"{i.file.name} - "
        line_num = str(i.line.number).zfill(file_digit_lengths.get(i.file, 0))
        print(f"[bold]{file_str}{line_num} > {i.line.content}[/bold]")


def display_warnings(warnings: WarningsObject):
    title_col = "bold yellow1"
    text_col = "orange3"
    for warning in warnings:
        print("---")
        if warning.stacktrace:
            stack_trace = "\n".join(listify_stack_nodes(warning.stacktrace))
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

        output.write_text("\n".join(compiled.output.get_ducky()))
        if compiled.sourcemap is not None:
            map_location = (output.parent / (output.stem + '.map'))
            map_location.write_text(json.dumps(compiled.sourcemap.to_dict()))
        return compiled


def listify_stack_nodes(nodes: list[StackTraceNode]):
    returnable: list[str] = ["-"]

    for i in nodes:
        if i.file:
            returnable.append(f"In file {i.file}, on line {i.line.number}:")
        else:
            returnable.append(f"On line {i.line.number}")

        returnable.append(f"> {i.line.content}")

        if i.line_2:
            returnable.append(f"Including line {i.line_2.number}:")
            returnable.append(f"> {i.line_2.content}")
        returnable.append("-")

    return returnable
