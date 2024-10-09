import geci_plots as gp
import matplotlib.pyplot as plt

from petrel_chicks.fit_model_for_peak_mass import fit_model_mass_vs_age, quadratic_function


def plot_peak_mass_model_and_data(df):
    _, ax = gp.geci_plot()

    plt.scatter(df.Edad, df.Masa)
    plt.plot(df.Edad, df.Masa)
    plt.ylabel("Mass $\\left( g \\right)$")
    plt.xlabel("Chick age $\\left( d \\right)$")
    return ax


def get_fitted_mass(df):
    parameters, _ = fit_model_mass_vs_age(df)
    return [quadratic_function(x, *parameters) for x in df.Edad]
