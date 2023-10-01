from rich.progress import Progress, SpinnerColumn, TextColumn
from ducklingscript import Compile
from typing import Annotated
from rich import print
import pkg_resources
import typer

app = typer.Typer()


@app.command()
def compile(
        filename: Annotated[typer.FileText, typer.Argument(help="The file to be compiled")],
        output: Annotated[str, typer.Option(help="The name of the newly compiled file")] = "a.txt"
    ):
    try:
        with Progress( SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True ) as progress:
            progress.add_task(description="Compiling...", total=None)
            compiled = Compile().parse(filename.read())
            with open(output, 'w') as f:
                f.write(str(compiled))
    except Exception as e:
        print(f"[bold red]{type(e).__name__}:[/bold red] {e.args[0]}")
    else:
        print(f"[bold green]Compilation complete![/bold green]")


@app.command()
def version():
    print(
        f"[dark_orange]{__package__}[/dark_orange] is version {pkg_resources.get_distribution(__package__).version}"
    )

if __name__ == "__main__":
    app()