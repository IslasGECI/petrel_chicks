from petrel_chicks import (
    get_fitted_mass,
    plot_peak_mass_model_and_data,
    quadratic_function,
    fit_model_mass_vs_age,
)
import pandas as pd
import matplotlib as plt


df = pd.DataFrame(
    {
        "ID_unico": ["c-2013", "c-2013", "c-2013", "c-2013", "c-2013"],
        "Temporada": [2013, 2013, 2013, 2013, 2013],
        "Masa": [5, 8, 0, 10, 8.1],
        "Edad": [0, 1, -1, 2, 3],
    }
)

expected_y_values = [
    -0.13428571428571434,
    5.157142857142857,
    8.334285714285713,
    9.397142857142857,
    8.345714285714283,
]


def test_plot_peak_mass_model():
    obtained_ax = plot_peak_mass_model_and_data(df)
    assert isinstance(obtained_ax, plt.axes._axes.Axes)

    obtained_y_label = obtained_ax.get_ylabel()
    expected_y_label = "Mass $\\left( g \\right)$"
    assert obtained_y_label == expected_y_label
    assert (obtained_ax._children[0]._offsets.data[:, 1] == df.Masa).all()

    obtained_y_label = obtained_ax.get_xlabel()
    expected_y_label = "Chick age $\\left( d \\right)$"
    assert obtained_y_label == expected_y_label

    assert isinstance(obtained_ax._children[1], plt.lines.Line2D)
    assert obtained_ax._children[1].get_data()[0][0] < obtained_ax._children[1].get_data()[0][-1]
    plt.pyplot.savefig("prueba.png")


def tests_get_fitted_mass():
    obtained = get_fitted_mass(df)
    assert len(obtained) == 5

    assert obtained == expected_y_values
