import pandas as pd
import numpy as np
from pandas._testing import assert_frame_equal

from petrel_chicks import (
    add_unique_id,
    calculate_effective_mass_loss,
    calculate_mass_diff,
    calculate_mass_loss_no_feed,
    calculate_mass_loss_after_feed,
    evaluate_mass_loss_no_feed,
    filter_meal_events,
    filter_post_meal_data,
)

d: dict = {
    "ID_nido": [1.0, 2.0, 3.0, 4.0],
    "Fecha": [4.0, 3.0, 2.0, 1.0],
    "Masa": [4.0, 3.0, 3.5, 3],
    "Hora": ["15:00", "16:00", "18:00", "19:00"],
}
data = pd.DataFrame(d)

d_0: dict = {
    "ID_nido": [1.0, 2.0, 3.0, 4.0],
    "Fecha": [4.0, 3.0, 2.0, 1.0],
    "Masa": [4.0, 3.0, 3.5, 3],
    "Hora": ["15:00", "16:00", "18:00", "19:00"],
    "Hora_dt": pd.to_datetime(["15:00", "16:00", "18:00", "19:00"]),
    "diff_hours": [np.nan, 1, 2, 1],
    "diff_weights": [np.nan, -1, 0.5, -0.5],
    "mass_loss_rate": [np.nan, 1, -0.25, 0.5],
}

expected_mass_loss_data = pd.DataFrame(d_0)


def tests_calculate_mass_diff():
    obtained_df = calculate_mass_diff(data)
    obtained_columns = list(obtained_df.keys())
    expected_columns = [
        "ID_nido",
        "Fecha",
        "Masa",
        "Hora",
        "Hora_dt",
        "diff_hours",
        "diff_weights",
        "mass_loss_rate",
    ]
    assert obtained_columns == expected_columns
    assert_frame_equal(obtained_df, expected_mass_loss_data)


d_1: dict = {
    "ID_nido": [1.0, 2.0],
    "Fecha": [4.0, 3.0],
    "Masa": [4.0, 3.0],
    "Hora": ["15:00", "16:00"],
    "Hora_dt": pd.to_datetime(["15:00", "16:00"]),
    "diff_hours": [np.nan, 1],
    "diff_weights": [np.nan, -1],
    "mass_loss_rate": [np.nan, 1],
}

expected_all_data = pd.DataFrame(d_1)

d_2: dict = {
    "ID_nido": [4.0],
    "Fecha": [1.0],
    "Masa": [3.0],
    "Hora": ["19:00"],
    "Hora_dt": pd.to_datetime(["19:00"]),
    "diff_hours": [1.0],
    "diff_weights": [-0.5],
    "mass_loss_rate": [0.5],
}

expected_post_meal = pd.DataFrame(d_2, index=[3])


def test_filter_post_meal_data():
    obtained_dataframe = calculate_mass_diff(data)
    obtained_all_data, obtained_post_meal = filter_post_meal_data(obtained_dataframe)
    assert_frame_equal(obtained_all_data, expected_all_data)
    assert_frame_equal(obtained_post_meal, expected_post_meal)


def test_add_unique_id():
    d = {
        "Id_nido": [1.0, 2.0, 3.0, 4.0],
        "Fecha": [4.0, 3.0, 2.0, 1.0],
        "Masa": [4.0, 3.0, 3.5, 3],
        "Hora": ["15:00", "16:00", "18:00", "19:00"],
        "Year": [2020, 2020, 2020, 2020],
    }
    data = pd.DataFrame(d)
    add_unique_id(data)


def test_calculate_mass_loss_no_feed():
    df_model = pd.DataFrame({"Alpha": [1, 2], "Beta": [3, 5]})
    hours = 4
    chicks_mass = 5
    expected_mass_loss_no_feed = -108
    obtained_mass_loss_no_feed = calculate_mass_loss_no_feed(df_model, hours, chicks_mass)
    assert obtained_mass_loss_no_feed == expected_mass_loss_no_feed
    expected_mass_loss_after_feed = -64
    obtained_mass_loss_after_feed = calculate_mass_loss_after_feed(df_model, hours, chicks_mass)
    assert obtained_mass_loss_after_feed == expected_mass_loss_after_feed


def test_evaluate_mass_loss_no_feed():
    df_data = pd.DataFrame({"diff_hours": [4, 2], "Masa": [5, 10]})
    df_model = pd.DataFrame({"Alpha": [1, 2], "Beta": [3, 5]})
    obtained = evaluate_mass_loss_no_feed(df_data, df_model)
    expected = pd.DataFrame(
        {"diff_hours": [4, 2], "Masa": [5, 10], "mass_loss_no_feed": [-108, -104]}
    )
    assert_frame_equal(obtained, expected)


def test_calculate_effective_mass_loss():
    df_data = pd.DataFrame({"diff_hours": [4, 2], "Masa": [5, 10]})
    df_model = pd.DataFrame({"Alpha": [1, 2], "Beta": [3, 5]})
    obtained = calculate_effective_mass_loss(df_data, df_model)
    expected = pd.DataFrame(
        {
            "diff_hours": [4, 2],
            "Masa": [5, 10],
            "mass_loss_no_feed_half": [-54, -52],
            "mass_loss_after_feed_half": [-32, -31],
            "effective_mass_loss": [-86, -83],
        }
    )
    assert_frame_equal(obtained, expected, check_dtype=False)


def test_filter_meal_events():
    df_data = pd.DataFrame({"diff_hours": [4, 2], "Masa": [5, 10], "diff_weights": [-110, -102]})
    df_model = pd.DataFrame({"Alpha": [1, 2], "Beta": [3, 5]})
    obtained = filter_meal_events(df_data, df_model)
    expected = pd.DataFrame(
        {"diff_hours": [2], "Masa": [10], "diff_weights": [-102], "mass_loss_no_feed": [-104]}
    )
    assert_frame_equal(
        obtained.reset_index(drop=True), expected.reset_index(drop=True), check_dtype=False
    )
