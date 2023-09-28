import typer
from typing import Annotated
from cli import Compile

app = typer.Typer()

@app.command()
def main(filename: Annotated[typer.FileText, typer.Argument(help="The file to be compiled")]):
    print(f'Filename retrieved: {filename}')

@app.command()
def compile(filename: Annotated[typer.FileText, typer.Argument(help="The file to be compiled")]):
    print(f"File name retrieved (compile command): {filename}")

if __name__=="__main__":
    app()