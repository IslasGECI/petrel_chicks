import geci_plots as gp
import matplotlib.pyplot as plt
import numpy as np

from petrel_chicks.fit_model_for_peak_mass import fit_model_mass_vs_age, quadratic_function


def plot_peak_mass_model_and_data(df):
    _, ax = gp.geci_plot()

    plt.scatter(df.Edad, df.Masa)
    age, predicted_mass = xxget_fitted_mass(df)

    plt.plot(age, predicted_mass)
    plt.ylabel("Mass $\\left( g \\right)$")
    plt.xlabel("Chick age $\\left( d \\right)$")
    return ax


def get_fitted_mass(df):
    parameters, _ = fit_model_mass_vs_age(df)
    age = np.linspace(df.Edad.min(), df.Edad.max(), len(df.Edad))
    return [quadratic_function(x, *parameters) for x in age]


def xxget_fitted_mass(df):
    age = np.linspace(df.Edad.min(), df.Edad.max(), len(df.Edad))
    predicted_mass = get_fitted_mass(df)
    return age, predicted_mass
