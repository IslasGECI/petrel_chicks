from petrel_chicks import (
    get_fitted_points,
    _plot_peak_mass_model_and_data,
    _plot_peak_mass_model_and_data_by_season,
)
from petrel_chicks.plot_peak_mass_model import plot_all_peak_mass_models

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


def test_plot_peak_mass_model_and_data_by_season():
    season = 2015
    df = pd.read_csv("tests/data/medidas_morfometricas_con_edades.csv")
    obtained_ax = _plot_peak_mass_model_and_data_by_season(df, season)
    obtained_rows = len(obtained_ax.get_children()[0].get_offsets().data)
    expected_rows = 27
    assert obtained_rows == expected_rows


def test_plot_peak_mass_model_and_data():
    obtained_ax = _plot_peak_mass_model_and_data(df)
    assert isinstance(obtained_ax, plt.axes._axes.Axes)

    assert_the_labes_are_right(obtained_ax)
    assert (obtained_ax.get_children()[0].get_offsets().data[:, 1] == df.Masa).all()

    assert_children_is_line_2d(obtained_ax.get_children()[1])
    assert (
        obtained_ax.get_children()[1].get_data()[0][0]
        < obtained_ax.get_children()[1].get_data()[0][-1]
    )
    expected_fontsize = 20.0
    assert obtained_ax.get_yaxis().get_label().get_fontsize() == expected_fontsize
    assert obtained_ax.get_xaxis().get_label().get_fontsize() == expected_fontsize
    assert obtained_ax.get_yticklabels()[1].get_fontsize() == expected_fontsize
    assert obtained_ax.get_xticklabels()[1].get_fontsize() == expected_fontsize
    assert obtained_ax.get_children()[0].get_alpha() == 0.5
    assert obtained_ax.get_children()[1].get_color() == "r"
    assert obtained_ax.get_legend().get_texts()[0].get_text() == "Measured bird mass"
    assert obtained_ax.get_legend().get_texts()[1].get_text() == "Fitted model"


def test_plot_plot_all_peak_mass_models():
    df = pd.read_csv("tests/data/medidas_morfometricas_con_edades.csv")
    obtained_ax = plot_all_peak_mass_models(df)
    plt.pyplot.savefig("test.png", transparent=True)
    children_index_for_each_season = [0, 1, 2]
    for nth_children in children_index_for_each_season:
        child_nth = obtained_ax.get_children()[nth_children]
        assert_children_is_line_2d(child_nth)
    assert obtained_ax.get_children()[0].get_data()[0][0] == 27
    assert obtained_ax.get_children()[1].get_data()[0][0] == 26
    assert obtained_ax.get_legend().get_texts()[0].get_text() == "Season 2013"
    assert obtained_ax.get_legend().get_texts()[1].get_text() == "Season 2015"
    assert_the_labes_are_right(obtained_ax)


def assert_children_is_line_2d(children):
    assert isinstance(children, plt.lines.Line2D)


def assert_the_labes_are_right(obtained_ax):
    obtained_y_label = obtained_ax.get_ylabel()
    expected_y_label = "Mass $\\left( g \\right)$"
    assert obtained_y_label == expected_y_label
    obtained_y_label = obtained_ax.get_xlabel()
    expected_y_label = "Chick age $\\left( d \\right)$"
    assert obtained_y_label == expected_y_label


def tests_get_fitted_mass():
    _, obtained = get_fitted_points(df)
    assert len(obtained) == 1000
