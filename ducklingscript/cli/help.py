from ducklingscript import Compiler

import typer
from typing import Annotated

from rich import print
from rich.markdown import Markdown
from rich.console import Console
from rich.style import Style

from ducklingscript.compiler.commands.bases.doc_command import ArgReqType, ComDoc


def help(
    command_name: Annotated[str, typer.Argument(help="The command to give a description on")]
):
    console = Console()

    com_doc = Compiler.get_docs(command_name)
    command = Compiler.get_command(command_name)

    if com_doc is None:
        print(f"[bold red]The command {command_name} does not exist. ⛔[/bold red]")
        return

    if com_doc.flipper_only:
        print(
            f"[royal_blue1]:exclamation: This command is flipper only! :exclamation:[/royal_blue1]"
        )

    print(f"[orchid]Names: {', '.join(com_doc.names)}[/orchid]")

    print_desc(console, com_doc)

    print(f"[orange3]{get_arg_req_text(com_doc.arg_req_type)}[/orange3]")

    if com_doc.parameters is not None:
        print(f"[gold3]Parameters: {com_doc.parameters}[/gold3]")

    if com_doc.arg_req_type != ArgReqType.NOTALLOWED:
        arg_type = com_doc.argument_type
        print(
            f"[yellow2]Argument type: {arg_type if isinstance(arg_type, str) else arg_type.__name__ }[/yellow2]"
        )

    print_examples(console, com_doc)


def get_arg_req_text(arg_req_type: ArgReqType) -> str:
    match (arg_req_type):
        case ArgReqType.REQUIRED:
            return "-> Argument(s) are required"
        case ArgReqType.ALLOWED:
            return "-> Argument(s) are allowed, but not required"
        case ArgReqType.NOTALLOWED:
            return "-> This command has no argument(s)"

def print_examples(console: Console, com_doc: ComDoc):
    if not com_doc.examples: return

    Console()

    print(f"[aquamarine1]{Markdown('# Examples')}")
    print("-->")
    print_md(console, "")

    for i in com_doc.examples:
        if i.file_structure:
            print_md(console, "## File Structure")

        print_md(console, "## DucklingScript")
        console.print(i.duckling)

        if i.compiled:
            print_md(console, "## Compiled")
            console.print(i.compiled)
        
        if i.std_out:
            print_md(console, "## Console Output")
            console.print(i.std_out)
        
        print("-->")
    

def print_desc(console: Console, com_doc: ComDoc):
    console.print(
        "[bold]Description: [/bold]", 
        Markdown(com_doc.description if com_doc.description else '[no description provided]'), 
        end='', style=Style(color="red"))

def print_md(console: Console, markup: str):
    console.print(Markdown(markup))