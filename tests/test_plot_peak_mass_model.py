from petrel_chicks import plot_peak_mass_model_and_data
import pandas as pd
import matplotlib as plt


def test_plot_peak_mass_model():
    df = pd.DataFrame(
        {
            "ID_unico": ["c-2013", "c-2013", "c-2013", "c-2013", "c-2013"],
            "Temporada": [2013, 2013, 2013, 2013, 2013],
            "Masa": [5, 8, 0, 10, 8.1],
            "Edad": [0, 1, -1, 2, 3],
        }
    )
    obtained_ax = plot_peak_mass_model_and_data(df)
    assert isinstance(obtained_ax, plt.axes._axes.Axes)

    obtained_y_label = obtained_ax.get_ylabel()
    expected_y_label = "Mass $\\left( g \\right)$"
    assert obtained_y_label == expected_y_label
    assert (obtained_ax._children[0]._offsets.data[:, 1] == df.Masa).all()

    obtained_y_label = obtained_ax.get_ylabel()
    expected_y_label = "Chick age $\\left( d \\right)$"
    assert obtained_y_label == expected_y_label
