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
)
from rich import print
from rich.progress import Progress

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

        compile_comp = CompileComponent.get()
        progress.update(main_task, description="Compiling...")
        compiled = compile_comp.prepare_and_compile(
            filename, compile_options=CompileOptions(**config)
        )

        ducky = compiled.output
        progress.update(main_task, description="Waiting...")
        quack_config = QuackConfig(delay=delay)
        try:
            progress.start_task(main_task)
            progress.update(main_task, description="Running...", total=len(ducky))
            interpreter = QuackInterpreter(
                [create_between_lines(progress, main_task)], config=quack_config
            )
            interpreter.interpret_text("\n".join(ducky))
        except FailSafeException:
            print(
                "[bold red]Failsafe triggered by putting mouse in the corner of the screen. Exiting...[/bold red]"
            )
