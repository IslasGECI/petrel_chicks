from petrel_chicks import get_fitted_points, plot_peak_mass_model_and_data
import pandas as pd
import matplotlib as plt


df = pd.DataFrame(
    {
        "ID_unico": [
            "c-2013",
            "c-2013",
            "c-2013",
            "c-2013",
            "d-2013",
            "d-2013",
            "d-2013",
            "c-2013",
            "c-2013",
            "c-2013",
        ],
        "Temporada": [2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013],
        "Masa": [5, 8, 0, 10, 8.1, 5, 8, 10, 15, 20],
        "Edad": [0, 1, -1, 2, 3, 1, 3, 5, 7, 9],
    }
)


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
    expected_fontsize = 20.0
    assert obtained_ax.get_yaxis().get_label().get_fontsize() == expected_fontsize
    assert obtained_ax.get_xaxis().get_label().get_fontsize() == expected_fontsize
    assert obtained_ax.get_yticklabels()[1].get_fontsize() == expected_fontsize
    assert obtained_ax.get_xticklabels()[1].get_fontsize() == expected_fontsize
    assert obtained_ax.get_children[1].get_alpha() == 0.5
    plt.pyplot.savefig("prueba.png")


def tests_get_fitted_mass():
    _, obtained = get_fitted_points(df)
    assert len(obtained) == 1000
