from pathlib import Path
from quackinter.line import Line as QuackLine
from quackinter.stack import Stack as QuackStack
import typer
from typing import Annotated
from quackinter import (
    Config as QuackConfig,
    QuackinterError,
)
from rich import print
from rich.progress import Progress

from ..interpreter.interpreter import DucklingInterpreter

from ..compiler.errors import DucklingScriptError, StackTraceNode, WarningsObject

from ..compiler.compiler import Compiled

from ..compiler.compile_options import CompileOptions

from .components.compile_component import CompileComponent
from .utils import Configuration

filename_type = Annotated[
    Path,
    typer.Argument(
        help="The file to be compiled and interpreted",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
]


def interpret(
    filename: filename_type,
    stack_limit: Annotated[
        int,
        typer.Option(
            help="The max amount of stacks allowed in your program", min=5, max=200
        ),
    ] = Configuration.config.stack_limit,
    delay: Annotated[
        int,
        typer.Option(help="How long in milliseconds to wait before we run the script."),
    ] = 1000,
):
    """
    Compile a DucklingScript file, and execute it
    """
    with Progress() as progress:
        main_task = progress.add_task("Loading config...", False, delay)
        config = Configuration.config.to_dict()
        config["stack_limit"] = stack_limit
        config["create_sourcemap"] = False

        compile_comp = CompileComponent.get()
        progress.update(main_task, description="Compiling...")

        def on_compilation_failure(error: DucklingScriptError):
            progress.remove_task(main_task)
            compile_comp.compile_with_error(error)

        def on_compilation_successful(warnings: WarningsObject, compiled: Compiled):
            compile_comp.display_warnings(warnings)
            progress.start_task(main_task)
            progress.update(
                main_task, description="Running...", total=len(compiled.output)
            )

        def while_interpretation(
            line_count: int, total_lines: int, stack: QuackStack, line: QuackLine
        ):
            progress.update(main_task, advance=1)

        def on_interpretation_failure(
            error: QuackinterError, duckling_stacktrace: list[StackTraceNode]
        ):
            progress.stop_task(main_task)
            display_interpret_error(error, duckling_stacktrace)

        def on_internal_error(error: Exception):
            progress.stop_task(main_task)
            progress.print(
                "[red]Interpret cancelled due to an internal error ❌[/red]", emoji=True
            )

        def on_fail_safe():
            progress.stop_task(main_task)
            print(
                "[bold red]Failsafe triggered by putting mouse in the corner of the screen. Exiting...[/bold red]"
            )

        quack_config = QuackConfig(
            delay=delay, output=lambda output, line: print(f"-> {output}")
        )

        interpreter = DucklingInterpreter(
            compile_options=CompileOptions(**config), quack_config=quack_config
        )
        interpreter.on_compilation_successful(on_compilation_successful)
        interpreter.on_compilation_failure(on_compilation_failure)
        interpreter.while_interpretation(while_interpretation)
        interpreter.on_interpretation_failure(on_interpretation_failure)
        interpreter.on_fail_safe(on_fail_safe)
        interpreter.on_internal_error(on_internal_error)

        interpreter.interpret_file(filename)


def display_interpret_error(
    error: QuackinterError, duckling_stacktrace: list[StackTraceNode]
):
    compile_comp = CompileComponent.get()

    stacktrace_error_str = "\n".join(
        compile_comp.listify_stack_nodes(duckling_stacktrace)
    )
    print("---\n[bright_red bold] -> Stacktrace[/bright_red bold]")
    print(f"[red]{stacktrace_error_str}[/red]")
    print(f"[bold red]{type(error).__name__}:[/bold red] {error.args[0]}")
    print("---\n[bold bright_red]Run failed with an error.[/bold bright_red] ⛔")
    print("---")
