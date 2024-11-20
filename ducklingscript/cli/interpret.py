from pathlib import Path
from pyautogui import FailSafeException
from quackinter.line import Line
from quackinter.stack import Stack
import typer
from typing import Annotated, Any
from quackinter import (
    Interpreter as QuackInterpreter,
    Config as QuackConfig,
    Command as QuackCommand,
    QuackinterError,
    InterpreterReturn,
)
from rich import print
from rich.progress import Progress

from ..compiler.errors import DuckyScriptError

from ..compiler.compiler import Compiled

from ..compiler.sourcemapping.sourcemap import SourceMap

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


def create_between_lines(progress: Progress, task: Any):
    class BetweenLinesCommand(QuackCommand):
        names = []

        def tick(self, stack: Stack, line: Line) -> None:
            progress.update(task, advance=1)

        def execute(self, stack: Stack, cmd: str, data: str) -> None:
            return None

    return BetweenLinesCommand


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
        config["create_sourcemap"] = True

        progress.update(main_task, description="Compiling...")
        compiled = compile_with_protection(filename, CompileOptions(**config))
        if compiled is None:
            progress.remove_task(main_task)
            progress.print("[red]Interpret cancelled due to error ❌[/red]", emoji=True)
            return

        ducky = compiled.output
        progress.update(main_task, description="Waiting...")
        quack_config = QuackConfig(
            delay=delay, output=lambda output: print(f"-> {output}")
        )
        return_data = None
        try:
            progress.start_task(main_task)
            progress.update(main_task, description="Running...", total=len(ducky))
            interpreter = QuackInterpreter(
                [create_between_lines(progress, main_task)], config=quack_config
            )
            return_data = interpreter.interpret_text("\n".join(ducky))
        except FailSafeException:
            print(
                "[bold red]Failsafe triggered by putting mouse in the corner of the screen. Exiting...[/bold red]"
            )
            return
        except QuackinterError as e:
            print(
                f'[bold red]An error occurred inside of Quackinter.\n{type(e).__name__}[/bold]: "{e.args[0]}"[/red]'
            )
            return

        if return_data.error:
            assert compiled.sourcemap, "Sourcemap is supposed to be available here"
            error_while_interpret(return_data, compiled.sourcemap)


def compile_with_protection(
    file_path: Path, options: CompileOptions
) -> Compiled | None:
    compile_comp = CompileComponent.get()
    try:
        return compile_comp.prepare_and_compile(file_path, compile_options=options)
    except DuckyScriptError as e:
        compile_comp.compile_with_error(e)
    return None


def error_while_interpret(data: InterpreterReturn, sourcemap: SourceMap):
    if not data.error or not data.stacktrace:
        return

    ducky_stacktrace = sourcemap.get_stacktrace_from(
        data.stacktrace.traceback[-1].line_num
    )
    compile_comp = CompileComponent.get()

    stacktrace_error_str = "\n".join(compile_comp.listify_stack_nodes(ducky_stacktrace))
    print(f"[red]{stacktrace_error_str}[/red]")
    print(
        f"[bold red]{type(data.stacktrace.error).__name__}:[/bold red] {data.stacktrace.error.args[0]}"
    )
    print("---\n[bold bright_red]Run failed with an error.[/bold bright_red] ⛔")
    print("---")
