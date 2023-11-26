from ducklingscript import Compiler

import typer
from typing import Annotated

from rich import print
from rich.markdown import Markdown
from rich.console import Console
from rich.style import Style
from rich.markup import escape

from ..compiler.commands.bases.simple_command import SimpleCommand
from ..compiler.commands.bases.base_command import BaseCommand

from ducklingscript.compiler.commands.bases.doc_command import ArgReqType, ComDoc

class HelpConsole(Console):
    def print_md(self, markup: str, color: str|None=None):
        self.print(Markdown(markup), style=Style(color=color))

    def print_labeled(self, label: str, text: str, color: str|None = None, extraline: bool = True, markdown: bool = True):
        new_line = '' if extraline else None
        if markdown:
            self.print_color(
                f"[bold]{label}: ",Markdown(text.strip()),new_line,color=color
            )
        else:
            self.print_color(
                f"[bold]{label}:\n",text.strip(),'\n'if extraline else '',color=color
            )

    def print_color(self, *text: object, color: str|None = None, markup: bool = True):
        self.print(
            *text,style=Style(color=color), markup=markup 
        )



def help(
    command_name: Annotated[str, typer.Argument(help="The command to give a description on")],
    examples: Annotated[bool, typer.Option(help="Give examples of the command")] = False
):
    console = HelpConsole()

    com_doc = Compiler.get_docs(command_name)
    command = Compiler.get_command(command_name)

    if com_doc is None or command is None:
        print(f"[bold red]The command {command_name} does not exist. ⛔[/bold red]")
        return
    
    if not examples:
        print_command(console, com_doc, command)
    else:
        print_examples(console, com_doc)


def print_command(console: HelpConsole, com_doc: ComDoc, command: type[BaseCommand]):
    console.print_color(f":wrench: This command is a {command.__base__.__name__}", color="deep_sky_blue3")

    if com_doc.flipper_only:
        console.print_color(
            ":exclamation: This command is flipper only! :exclamation:", 
            color="royal_blue1"
        )

    console.print_color(
        get_arg_req_text(com_doc.arg_req_type),
        color="orange3"
    )

    console.print_labeled("Names", ', '.join(com_doc.names), "orchid")

    console.print_labeled(
        "Description", 
        com_doc.description if com_doc.description else '[no description provided]', 
        'red'
    )

    if com_doc.parameters is not None:
        console.print_labeled(
            "Parameters",
            ", ".join(com_doc.parameters),
            "gold3"
        )

    if com_doc.arg_req_type != ArgReqType.NOTALLOWED:
        arg_type = com_doc.argument_type
        console.print_labeled(
            label="Argument type",
            text=arg_type if isinstance(arg_type, str) else arg_type.__name__,
            color="yellow2",
            markdown=False
        )
    
    if com_doc.examples:
        console.print_color("[THIS COMMAND HAS EXAMPLES. Use --examples]", color="orange3")


def get_arg_req_text(arg_req_type: ArgReqType) -> str:
    match (arg_req_type):
        case ArgReqType.REQUIRED:
            return "-> Argument(s) are required"
        case ArgReqType.ALLOWED:
            return "-> Argument(s) are allowed, but not required"
        case ArgReqType.NOTALLOWED:
            return "-> This command has no argument(s)"

def print_examples(console: HelpConsole, com_doc: ComDoc):
    if not com_doc.examples: 
        console.print_color("[bold red]This command does not have examples. ⛔[/bold red]")
        return

    for example_count,i in enumerate(com_doc.examples):
        print(f"[bold yellow1]--> Example {example_count}")
        if i.file_structure:
            console.print_labeled(
                "File Structure",
                "```"+i.file_structure+"```"
            )

        console.print_labeled(
            "DucklingScript",
            "```"+i.duckling+"```",
            color="blue"
        )

        if i.compiled:
            console.print_labeled(
                "Compiled",
                "```"+i.compiled+"```"
            )
        
        if i.std_out:
            console.print_labeled(
                "Console Output",
                "```"+i.std_out+"```",
                color="aquamarine"
            )
        
    print("-->")
