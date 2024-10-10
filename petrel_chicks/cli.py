import typer

cli = typer.Typer()


@cli.command()
def version():
    print("version")
