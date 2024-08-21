from petrel_chicks.fit_model_for_peak_mass import (
    find_age_for_max_mass_from_data,
    calculate_max_weights_from_given_age,
    calculate_peak_mass_from_model_by_season,
)

import pandas as pd
import numpy as np


ages_and_mass = pd.DataFrame({"ID": ["a", "a", "a"], "Masa": [5, 8, 0], "Edad": [0, 1, -1]})


def test_find_age_for_max_mass_from_data():
    obtained_age = find_age_for_max_mass_from_data(ages_and_mass)
    expected_age = 2
    assert obtained_age == expected_age

    ages_and_mass_with_na = pd.DataFrame(
        {"ID": ["a", "a", "a", "b"], "Masa": [8, 21, 0, np.NaN], "Edad": [0, 1, -1, 3]}
    )
    obtained_age = find_age_for_max_mass_from_data(ages_and_mass_with_na)
    assert isinstance(obtained_age, int)


def test_calculate_max_weights_from_given_age():
    df = pd.DataFrame({"ID_unico": ["a", "b", "b"], "Masa": [5, 8, 0], "Edad": [1, 1, 3]})
    age = 1
    obtained = calculate_max_weights_from_given_age(df, age)
    assert len(obtained) == 2
    age = 3
    obtained = calculate_max_weights_from_given_age(df, age)
    assert len(obtained) == 2
    assert np.isnan(obtained.Peak_mass[0])


def test_calculate_peak_mass_from_model_by_season():
    df = pd.DataFrame(
        {
            "ID_unico": ["c-2013", "c-2013", "c-2013", "c-2013", "c-2013"],
            "Temporada": [2013, 2013, 2013, 2013, 2013],
            "Masa": [5, 8, 0, 10, 8.1],
            "Edad": [0, 1, -1, 2, 3],
        }
    )
    obtained = calculate_peak_mass_from_model_by_season(df)
    assert (obtained[obtained.ID_unico == "c-2013"].Peak_mass == 10).all()
    df_other_season = pd.DataFrame(
        {
            "ID_unico": ["c-2014", "c-2014", "c-2014", "a-2014", "a-2014"],
            "Temporada": [2014, 2014, 2014, 2014, 2014],
            "Masa": [5, 8, 0, 10, 8.1],
            "Edad": [2, 3, 1, 4, 5],
        }
    )
    df_two_seasons = pd.concat([df, df_other_season], ignore_index=True)
    obtained = calculate_peak_mass_from_model_by_season(df_two_seasons)
    assert (obtained[obtained.ID_unico == "a-2014"].Peak_mass == 10).all()
    assert len(obtained) == 3
    assert (obtained[obtained.ID_unico == "c-2013"].Peak_mass == 10).all()
