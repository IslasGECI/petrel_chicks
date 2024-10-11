import matplotlib.pyplot as plt
import pandas as pd
import typer

from petrel_chicks.plot_peak_mass_model import _plot_peak_mass_model_and_data

cli = typer.Typer()


@cli.command()
def plot_peak_mass_model(
    data_path: str = typer.Option("", help="Input file path"),
    season: int = typer.Option("", help="Season"),
    output_path: str = typer.Option("", help="Output file path"),
):
    data = pd.read_csv(data_path)
    _plot_peak_mass_model_and_data(data)
    plt.savefig(output_path)


@cli.command()
def version():
    print("version")
