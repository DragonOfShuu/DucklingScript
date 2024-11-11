from __future__ import annotations

import json
from pathlib import Path
from rich import print

from .cli_component import CliComponent

from ...compiler.compile_options import CompileOptions
from ...compiler.compiled_ducky import StdOutData
from ...compiler.compiler import Compiled, Compiler
from ...compiler.errors import CompilationError, GeneralError, StackTraceNode, WarningsObject

class CompileComponent(CliComponent):
    @classmethod
    def get(cls) -> CompileComponent:
        if cls._component:
            return cls._component
        new_component = cls()
        cls._component = new_component
        return new_component

    def compile_with_error(self, e: CompilationError):
        if isinstance(e, GeneralError):
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


    def print_std_out(self, obj: Compiled | CompilationError):
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


    def prepare_and_compile(
        self, filename: Path, output: Path|None = None, compile_options: CompileOptions|None = None
    ):
        compiled = Compiler(compile_options).compile_file(filename)
        self.display_warnings(compiled.warnings)

        if not output:
            return compiled

        output.write_text("\n".join(compiled.output))
        if compiled.sourcemap is not None:
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
