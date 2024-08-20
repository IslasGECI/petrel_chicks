from petrel_chicks.fit_model_for_peak_mass import (
    find_age_for_max_mass_from_data,
    calculate_max_weights_from_given_age,
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
