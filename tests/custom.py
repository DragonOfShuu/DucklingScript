from pathlib import Path
from typing import Any
from rich import print
from rich.progress import Progress
import traceback

from quackinter.config import Config

from ducklingscript import DucklingInterpreter, Compiled, WarningsObject
from ducklingscript.cli.components import CompileComponent
from ducklingscript.compiler.compile_options import CompileOptions


CUSTOM_SCRIPT_FOLDER_NAME = "custom_test_scripts"
CUSTOM_SCRIPT_LOCATION = Path(__file__).parent / CUSTOM_SCRIPT_FOLDER_NAME


def run_test(index: int = 1):
    config = Config(
        delay=1000, output=lambda output, line: print(f"{line.line_num} -> {output}")
    )

    compile_options = CompileOptions(
        quackinter_commands=True,
    )

    ducky_code = CUSTOM_SCRIPT_LOCATION / f"custom{index}.dkls"
    if not ducky_code.exists:
        print("File index given does not exist.")
        return

    with Progress() as progress:
        compile_task = progress.add_task("Compile", start=False)
        interpret_task = progress.add_task("Interpret", False, visible=False)

        def compile_success(warnings: WarningsObject, compiled: Compiled):
            CompileComponent.get().display_warnings(warnings)
            progress.start_task(compile_task)
            progress.update(compile_task, total=1, completed=1)
            progress.update(interpret_task, visible=True, total=len(compiled.compiled))
            progress.start_task(interpret_task)
            progress.print("Await 1 second...")

        def while_interpret(
            line_count: int,
            total_lines: int,
            stack: Any,
            line: Any,
        ):
            if not interpret_task:
                return
            progress.update(interpret_task, completed=line_count)

        interpreter = DucklingInterpreter(
            quack_config=config, compile_options=compile_options
        )
        interpreter.on_compilation_failure(
            lambda error: CompileComponent.get().compile_with_error(error)
        )
        interpreter.on_compilation_successful(compile_success)
        interpreter.on_fail_safe(
            lambda: print("[bold red]FAILSAFE TRIGGERED. Exiting...[/bold red]")
        )
        interpreter.on_internal_error(
            lambda error: print(
                f"[bold red]INTERNAL ERROR: {error.__class__.__name__}:[/bold red] {error}\n{''.join(traceback.TracebackException.from_exception(error).format())}"
            )
        )
        interpreter.on_interpretation_failure(CompileComponent.get().interpret_error)
        interpreter.while_interpretation(while_interpret)

        interpreter.interpret_file(ducky_code)


def generate_tests():
    CUSTOM_SCRIPT_LOCATION.mkdir(exist_ok=True)
    custom1 = CUSTOM_SCRIPT_LOCATION / "custom1.dkls"
    custom1.write_text(
        """
FUNC powershell
    WIN r
    DELAY 500
    STRINGLN powershell
    DELAY 1000

RUN powershell
STRINGLN notepad
DELAY 1000
CTRL t
DELAY 500
DEFAULTSTRINGDELAY 20
STRINGLN
    \"\"\"
    --->
    DUCKLINGSCRIPT
    --->

    A programming language built for injecting
    key strokes.
    \"\"\"
"""
    )
    print(
        'Generation complete! Run "poetry run poe test" to run! (only runs DuckyScript right now)'
    )
