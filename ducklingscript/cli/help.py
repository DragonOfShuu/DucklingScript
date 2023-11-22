from ducklingscript import Compiler

from typer import Argument
from rich import print
from typing import Annotated

from ..compiler.commands.bases.doc_command import ArgReqType

def help(command: Annotated[str, Argument(help="The command to give a description on")]):
    com_doc = Compiler.get_docs(command)
    if com_doc is None:
        print(f"[bold red]The command {command} does not exist. ⛔[/bold red]")
        return

    print(f"[orchid]Names: {', '.join(com_doc.names)}[/orchid]")
    print(f"[red]Description: {com_doc.description}[/red]")
    print(f"[orange3]{get_arg_req_text(com_doc.arg_req_type)}[/orange3]")
    if com_doc.parameters is not None:
        print(f"[gold3]Parameters: {com_doc.parameters}[/gold3]")
    if com_doc.arg_req_type!=ArgReqType.NOTALLOWED:
        print(f"[yellow2]Argument type: {com_doc.argument_type}[/yellow2]")
    
    if (com_doc.example_duckling is not None) and (com_doc.example_compiled is not None):
        print(f"[aquamarine1]Examples:")

        if com_doc.example_duckling is not None:
            print("DucklingScript examples:")
            for example in com_doc.example_duckling:
                print(f"{example}")
        if com_doc.example_compiled is not None:
            print("Compiled:")
            for example in com_doc.example_compiled:
                print(f"{example}")
        
        print(f"[/aquamarine1]")

def get_arg_req_text(arg_req_type: ArgReqType) -> str:
    match (arg_req_type):
        case ArgReqType.REQUIRED:
            return "-> Argument(s) are required"
        case ArgReqType.ALLOWED:
            return "-> Argument(s) are allowed, but not required"
        case ArgReqType.NOTALLOWED:
            return "-> This command has no argument(s)"