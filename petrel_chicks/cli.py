import typer

cli = typer.Typer()


@cli.command()
def plot_peak_mass_model(
    data_path: str = typer.Option("", help="Input file path"),
    season: int = typer.Option("", help="Season"),
):
    pass


@cli.command()
def version():
    print("version")
