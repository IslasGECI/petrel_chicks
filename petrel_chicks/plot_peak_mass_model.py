import geci_plots as gp
import matplotlib.pyplot as plt
import numpy as np

from petrel_chicks.fit_model_for_peak_mass import fit_model_mass_vs_age, quadratic_function


def plot_peak_mass_model_and_data(df):
    _, ax = gp.geci_plot()
    fontsize = 20

    plt.scatter(df.Edad, df.Masa, alpha=0.5)
    age, predicted_mass = get_fitted_points(df)

    plt.plot(age, predicted_mass)
    plt.ylabel("Mass $\\left( g \\right)$", fontsize=fontsize)
    plt.xlabel("Chick age $\\left( d \\right)$", fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    return ax


def get_fitted_mass(df, age):
    parameters, _ = fit_model_mass_vs_age(df)
    return [quadratic_function(x, *parameters) for x in age]


def get_fitted_points(df):
    age = np.linspace(df.Edad.min(), df.Edad.max(), 1000)
    predicted_mass = get_fitted_mass(df, age)
    return age, predicted_mass
