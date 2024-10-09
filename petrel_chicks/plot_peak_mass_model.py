import geci_plots as gp
import matplotlib.pyplot as plt


def plot_peak_mass_model_and_data(df):
    _, ax = gp.geci_plot()

    ax.scatter(df.Edad, df.Masa)
    plt.ylabel("Mass $\\left( g \\right)$")
    return ax
