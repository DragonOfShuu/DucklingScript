from __future__ import annotations

import json
from pathlib import Path
from rich import print

from quackinter import QuackinterError

from .cli_component import CliComponent
from ...compiler.compile_options import CompileOptions
from ...compiler.compiled_ducky import StdOutData
from ...compiler.compiler import Compiled, DucklingCompiler
from ...compiler.errors import (
    DucklingScriptError,
    CompilationError,
    StackTraceNode,
    WarningsObject,
)


class CompileComponent(CliComponent):
    @classmethod
    def get(cls) -> CompileComponent:
        if cls._component:
            return cls._component
        new_component = cls()
        cls._component = new_component
        return new_component

    def compile_with_error(self, e: DucklingScriptError):
        if isinstance(e, CompilationError):
            all_error = "\n".join(self.listify_stack_nodes(e.stack_traceback(5)))
            print(f"[red]{all_error}[/red]")
        print(f"[bold red]{type(e).__name__}:[/bold red] {e.args[0]}")
        print("---\n[bold bright_red]Compile failed with an error.[/bold bright_red] ⛔")
        self.print_std_out(e)
        print("---")

    def compile_successful(self, compiled: Compiled):
        print("[bold green]Compilation complete![/bold green] ✨")
        if warn := compiled.warnings:
            print(
                f"[orange3](with {len(warn)} warning{'s' if len(warn)>1 else ''})[/orange3]"
            )
        self.print_std_out(compiled)
        print("---")

    def interpret_error(
        self, error: QuackinterError, duckling_stacktrace: list[StackTraceNode]
    ):
        stacktrace_error_str = "\n".join(self.listify_stack_nodes(duckling_stacktrace))
        print("---\n[bright_red bold] -> Stacktrace[/bright_red bold]")
        print(f"[red]{stacktrace_error_str}[/red]")
        print(f"[bold red]{type(error).__name__}:[/bold red] {error.args[0]}")
        print("---\n[bold bright_red]Run failed with an error.[/bold bright_red] ⛔")
        print("---")

    def print_std_out(self, obj: Compiled | DucklingScriptError):
        if not isinstance(obj, (Compiled, CompilationError)):
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
        self.print_std_data(data)

    def print_std_data(self, data: list[StdOutData]):
        file_digit_lengths = {}
        for i in data:
            if i.file is not None and file_digit_lengths.get(i.file) is None:
                file_length = len(i.file.open().readlines())
                digit_length = len(str(file_length))
                file_digit_lengths.update({i.file: digit_length})

            file_str = "" if i.file is None else f"{i.file.name} - "
            line_num = str(i.line.number).zfill(file_digit_lengths.get(i.file, 0))
            print(f"[bold]{file_str}{line_num} > {i.line.content}[/bold]")

    def display_warnings(self, warnings: WarningsObject):
        title_col = "bold yellow1"
        text_col = "orange3"
        for warning in warnings:
            print("---")
            if warning.stacktrace:
                stack_trace = "\n".join(self.listify_stack_nodes(warning.stacktrace))
                print(f"[{title_col}] -> Stacktrace[/{title_col}]")
                print(f"[{text_col}]{stack_trace}[/{text_col}]")
            print(f"[{title_col}] -> Warning[/{title_col}]")
            print(f"[{text_col}]{warning.error}[/{text_col}]")

    def compile_success_with_warnings(
        self, warnings: WarningsObject, compiled: Compiled
    ):
        self.display_warnings(warnings)
        self.compile_successful(compiled)

    def prepare_and_compile(
        self,
        filename: Path,
        output: Path | None = None,
        write_out_sourcemap: bool = True,
        compile_options: CompileOptions | None = None,
    ):
        compiled = DucklingCompiler(compile_options).compile_file(filename)
        self.display_warnings(compiled.warnings)

        if not output:
            return compiled

        output.write_text("\n".join(compiled.output))
        if compiled.sourcemap is not None and write_out_sourcemap:
            map_location = output.parent / (output.stem + ".map.json")
            map_location.write_text(json.dumps(compiled.sourcemap.to_dict(), indent=4))
        return compiled

    def listify_stack_nodes(self, nodes: list[StackTraceNode]):
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
