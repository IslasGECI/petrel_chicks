import geci_plots as gp
import matplotlib.pyplot as plt


def plot_peak_mass_model_and_data(df):
    _, ax = gp.geci_plot()

    plt.scatter(df.Edad, df.Masa)
    plt.ylabel("Mass $\\left( g \\right)$")
    plt.xlabel("Chick age $\\left( d \\right)$")
    return ax
